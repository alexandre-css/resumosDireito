# -*- coding: utf-8 -*-
"""
Servidor Web para Editor de Súmulas com edição direta dos arquivos JSON
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import subprocess
from urllib.parse import parse_qs
import webbrowser
from threading import Timer

class EditorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(self.get_html().encode('utf-8'))
            
        elif self.path.startswith('/api/sumulas/'):
            tribunal = self.path.split('/')[-1]
            if tribunal in ['stf', 'stj', 'eca']:
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                arquivo = f'Data/{tribunal}.json'
                if os.path.exists(arquivo):
                    with open(arquivo, 'r', encoding='utf-8') as f:
                        self.wfile.write(f.read().encode('utf-8'))
                else:
                    self.wfile.write(json.dumps({'sumulas': []}).encode('utf-8'))
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        if self.path.startswith('/api/sumulas/'):
            tribunal = self.path.split('/')[-1]
            if tribunal in ['stf', 'stj', 'eca']:
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    
                    # Salvar arquivo JSON
                    arquivo = f'Data/{tribunal}.json'
                    with open(arquivo, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'success': True}).encode('utf-8'))
                except Exception as e:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        
        elif self.path == '/api/gerar-html':
            try:
                # Executar o script Python diretamente sem o .bat
                import locale
                import sys
                system_encoding = locale.getpreferredencoding()
                
                # Usar o mesmo Python que está rodando o servidor
                python_exe = sys.executable
                
                result = subprocess.run(
                    [python_exe, 'Scripts/2_gerar_html.py'],
                    capture_output=True,
                    text=True,
                    encoding=system_encoding,
                    errors='replace',
                    timeout=30  # Timeout de 30 segundos
                )
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                # Verificar se houve erro
                success = result.returncode == 0
                
                self.wfile.write(json.dumps({
                    'success': success,
                    'output': result.stdout,
                    'error': result.stderr if not success else ''
                }, ensure_ascii=False).encode('utf-8'))
            except subprocess.TimeoutExpired:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Timeout: operação demorou muito'}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        # Silenciar logs
        pass
    
    def get_html(self):
        return '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Editor de Súmulas - ResumosDireito</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .sumula-item {
            transition: all 0.2s;
        }
        .sumula-item:hover {
            transform: translateX(4px);
        }
    </style>
</head>
<body class="bg-gray-50">
    <div class="container mx-auto px-4 py-8 max-w-7xl">
        <header class="text-center mb-8">
            <h1 class="text-4xl font-bold text-blue-900 mb-2">📝 Editor de Súmulas</h1>
            <p class="text-gray-600">Edição direta com salvamento automático</p>
        </header>

        <!-- Seletor de Tribunal -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-8">
            <div class="flex gap-4 mb-4">
                <button onclick="selecionarTribunal('stf')" id="btn-stf"
                    class="flex-1 px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition font-semibold">
                    STF (<span id="count-stf">0</span>)
                </button>
                <button onclick="selecionarTribunal('stj')" id="btn-stj"
                    class="flex-1 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition font-semibold">
                    STJ (<span id="count-stj">0</span>)
                </button>
                <button onclick="selecionarTribunal('eca')" id="btn-eca"
                    class="flex-1 px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition font-semibold">
                    ECA (<span id="count-eca">0</span>)
                </button>
            </div>
            <button onclick="gerarHTML()" id="btn-gerar"
                class="w-full px-6 py-4 bg-green-600 text-white rounded-lg hover:bg-green-700 transition font-bold text-lg">
                🚀 Gerar HTML Atualizado
            </button>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- Lista de Súmulas -->
            <div class="lg:col-span-1 bg-white rounded-lg shadow-md p-6">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-xl font-bold text-gray-800">📋 Súmulas</h2>
                    <button onclick="novaSumula()" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-semibold">
                        ➕ Nova
                    </button>
                </div>
                <div id="lista-sumulas" class="space-y-2 max-h-[600px] overflow-y-auto">
                    <p class="text-gray-500 text-center py-8">Carregando...</p>
                </div>
            </div>

            <!-- Formulário -->
            <div class="lg:col-span-2 bg-white rounded-lg shadow-md p-6">
                <h2 class="text-2xl font-bold text-gray-800 mb-6">✏️ Editor</h2>
                
                <div id="mensagem-vazia" class="text-center py-12 text-gray-500">
                    <p class="text-lg mb-2">👈 Selecione uma súmula para editar</p>
                    <p class="text-sm">ou clique em "➕ Nova" para criar uma nova</p>
                </div>

                <form id="formulario" class="space-y-4 hidden">
                    <input type="hidden" id="indice-edicao" value="">
                    
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Número *</label>
                            <input type="number" id="numero" required
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Cor</label>
                            <select id="cor" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
                                <option value="red">🔴 Vermelho</option>
                                <option value="blue">🔵 Azul</option>
                                <option value="green">🟢 Verde</option>
                                <option value="purple">🟣 Roxo</option>
                                <option value="orange">🟠 Laranja</option>
                                <option value="pink">🌸 Rosa</option>
                                <option value="teal">🔷 Teal</option>
                                <option value="indigo">💙 Índigo</option>
                            </select>
                        </div>
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Título *</label>
                        <input type="text" id="titulo" required
                            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Texto *</label>
                        <textarea id="texto" required rows="6"
                            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"></textarea>
                    </div>

                    <div class="grid grid-cols-2 gap-4">
                        <label class="flex items-center space-x-2">
                            <input type="checkbox" id="vinculante" class="w-5 h-5">
                            <span class="text-sm font-medium">Vinculante</span>
                        </label>
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Chips</label>
                        <div class="space-y-2">
                            <label class="flex items-center space-x-2">
                                <input type="checkbox" value="ALTERADA" class="chip-checkbox w-4 h-4">
                                <span class="text-sm">ALTERADA</span>
                            </label>
                            <label class="flex items-center space-x-2">
                                <input type="checkbox" value="SUPERADA EM PARTE" class="chip-checkbox w-4 h-4">
                                <span class="text-sm">SUPERADA EM PARTE</span>
                            </label>
                        </div>
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Nota</label>
                        <textarea id="nota" rows="2"
                            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"></textarea>
                    </div>

                    <div class="flex gap-4 pt-4">
                        <button type="submit" class="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold">
                            💾 Salvar
                        </button>
                        <button type="button" onclick="excluirSumula()" class="px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 font-semibold">
                            🗑️ Excluir
                        </button>
                        <button type="button" onclick="cancelarEdicao()" class="px-6 py-3 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 font-semibold">
                            ✖️ Cancelar
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <script>
        let tribunalAtual = 'stf';
        let sumulas = [];

        async function carregarSumulas(tribunal) {
            try {
                const response = await fetch(`/api/sumulas/${tribunal}`);
                const data = await response.json();
                sumulas = data.sumulas || [];
                atualizarLista();
                atualizarContador();
            } catch (error) {
                mostrarToast('Erro ao carregar súmulas', 'error');
            }
        }

        function atualizarLista() {
            const lista = document.getElementById('lista-sumulas');
            if (sumulas.length === 0) {
                lista.innerHTML = '<p class="text-gray-500 text-center py-8">Nenhuma súmula</p>';
                return;
            }

            lista.innerHTML = sumulas.map((s, i) => `
                <div onclick="editarSumula(${i})" 
                    class="sumula-item p-3 border rounded-lg cursor-pointer hover:bg-gray-50 hover:border-blue-400">
                    <div class="flex items-center justify-between">
                        <div>
                            <span class="font-bold text-lg">${s.numero}</span>
                            <span class="ml-2 text-gray-700">${s.titulo}</span>
                        </div>
                        <div class="w-4 h-4 rounded-full bg-${s.cor}-500"></div>
                    </div>
                </div>
            `).join('');
        }

        async function atualizarContador() {
            for (const tribunal of ['stf', 'stj', 'eca']) {
                const response = await fetch(`/api/sumulas/${tribunal}`);
                const data = await response.json();
                document.getElementById(`count-${tribunal}`).textContent = (data.sumulas || []).length;
            }
        }

        function selecionarTribunal(tribunal) {
            tribunalAtual = tribunal;
            ['stf', 'stj', 'eca'].forEach(t => {
                const btn = document.getElementById(`btn-${t}`);
                btn.classList.toggle('ring-4', t === tribunal);
                btn.classList.toggle('ring-offset-2', t === tribunal);
            });
            carregarSumulas(tribunal);
            cancelarEdicao();
        }

        function novaSumula() {
            document.getElementById('mensagem-vazia').classList.add('hidden');
            document.getElementById('formulario').classList.remove('hidden');
            document.getElementById('indice-edicao').value = '';
            document.getElementById('formulario').reset();
            document.querySelectorAll('.chip-checkbox').forEach(cb => cb.checked = false);
        }

        function editarSumula(indice) {
            const sumula = sumulas[indice];
            document.getElementById('mensagem-vazia').classList.add('hidden');
            document.getElementById('formulario').classList.remove('hidden');
            document.getElementById('indice-edicao').value = indice;
            
            document.getElementById('numero').value = sumula.numero;
            document.getElementById('titulo').value = sumula.titulo;
            document.getElementById('texto').value = sumula.texto;
            document.getElementById('cor').value = sumula.cor;
            document.getElementById('vinculante').checked = sumula.vinculante || false;
            document.getElementById('nota').value = sumula.nota || '';
            
            document.querySelectorAll('.chip-checkbox').forEach(cb => {
                cb.checked = (sumula.chips || []).includes(cb.value);
            });
        }

        function cancelarEdicao() {
            document.getElementById('formulario').classList.add('hidden');
            document.getElementById('mensagem-vazia').classList.remove('hidden');
        }

        async function salvarSumula(sumula) {
            try {
                const data = {
                    tribunal: tribunalAtual.toUpperCase(),
                    total: sumulas.length,
                    sumulas: sumulas
                };
                
                const response = await fetch(`/api/sumulas/${tribunalAtual}`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                if (response.ok) {
                    mostrarToast('✓ Salvo com sucesso!', 'success');
                    await carregarSumulas(tribunalAtual);
                    cancelarEdicao();
                }
            } catch (error) {
                mostrarToast('Erro ao salvar', 'error');
            }
        }

        document.getElementById('formulario').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const chips = Array.from(document.querySelectorAll('.chip-checkbox:checked')).map(cb => cb.value);
            if (document.getElementById('vinculante').checked && !chips.includes('VINCULANTE')) {
                chips.unshift('VINCULANTE');
            }
            
            const sumula = {
                numero: parseInt(document.getElementById('numero').value),
                titulo: document.getElementById('titulo').value,
                texto: document.getElementById('texto').value,
                cor: document.getElementById('cor').value,
                vinculante: document.getElementById('vinculante').checked,
                chips: chips
            };
            
            const nota = document.getElementById('nota').value;
            if (nota) sumula.nota = nota;
            
            const indice = document.getElementById('indice-edicao').value;
            if (indice === '') {
                sumulas.push(sumula);
            } else {
                sumulas[parseInt(indice)] = sumula;
            }
            
            sumulas.sort((a, b) => a.numero - b.numero);
            await salvarSumula();
        });

        async function excluirSumula() {
            const indice = document.getElementById('indice-edicao').value;
            if (indice !== '' && confirm('Tem certeza que deseja excluir esta súmula?')) {
                sumulas.splice(parseInt(indice), 1);
                await salvarSumula();
            }
        }

        async function gerarHTML() {
            const btn = document.getElementById('btn-gerar');
            btn.disabled = true;
            btn.textContent = '⏳ Gerando...';
            
            try {
                const response = await fetch('/api/gerar-html', {method: 'POST'});
                const result = await response.json();
                
                if (result.success) {
                    mostrarToast('✓ HTML gerado com sucesso!', 'success');
                    setTimeout(() => {
                        alert('HTML atualizado!\\n\\nVerifique o arquivo penal-sumulas.html');
                    }, 500);
                } else {
                    mostrarToast('Erro: ' + result.error, 'error');
                }
            } catch (error) {
                mostrarToast('Erro ao gerar HTML', 'error');
            }
            
            btn.disabled = false;
            btn.textContent = '🚀 Gerar HTML Atualizado';
        }

        function mostrarToast(msg, tipo) {
            const cor = tipo === 'success' ? 'bg-green-600' : 'bg-red-600';
            const toast = document.createElement('div');
            toast.className = `fixed top-4 right-4 ${cor} text-white px-6 py-3 rounded-lg shadow-lg z-50`;
            toast.textContent = msg;
            document.body.appendChild(toast);
            setTimeout(() => {
                toast.style.opacity = '0';
                setTimeout(() => document.body.removeChild(toast), 300);
            }, 2000);
        }

        // Inicializar
        selecionarTribunal('stf');
        atualizarContador();
    </script>
</body>
</html>'''

def abrir_navegador():
    webbrowser.open('http://localhost:8080')

if __name__ == '__main__':
    PORT = 8080
    server = HTTPServer(('localhost', PORT), EditorHandler)
    
    print("=" * 80)
    print("🚀 SERVIDOR DO EDITOR DE SÚMULAS")
    print("=" * 80)
    print(f"\n✓ Servidor iniciado em: http://localhost:{PORT}")
    print("\n📝 Funcionalidades:")
    print("   • Editar súmulas diretamente nos arquivos JSON")
    print("   • Adicionar e excluir súmulas")
    print("   • Gerar HTML com um clique")
    print("   • Salvamento automático")
    print("\n⚠️  Para encerrar: Pressione Ctrl+C")
    print("=" * 80)
    print()
    
    # Abrir navegador após 1 segundo
    Timer(1.0, abrir_navegador).start()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✓ Servidor encerrado")
