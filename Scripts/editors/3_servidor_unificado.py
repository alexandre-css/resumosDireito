# -*- coding: utf-8 -*-
"""
Editor Unificado - Súmulas e Temas com Git Integration
Permite editar súmulas e temas em uma única interface + Commit/Push Git
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import subprocess
from datetime import datetime
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
        
        elif self.path.startswith('/api/temas/'):
            tribunal = self.path.split('/')[-1]
            if tribunal in ['stf', 'stj']:
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                arquivo = f'Data/temas_{tribunal}.json'
                if os.path.exists(arquivo):
                    with open(arquivo, 'r', encoding='utf-8') as f:
                        self.wfile.write(f.read().encode('utf-8'))
                else:
                    self.wfile.write(json.dumps({'temas': []}).encode('utf-8'))
        
        elif self.path == '/api/categorias':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            arquivo = 'Data/categorias_cores.json'
            if os.path.exists(arquivo):
                with open(arquivo, 'r', encoding='utf-8') as f:
                    self.wfile.write(f.read().encode('utf-8'))
            else:
                self.wfile.write(json.dumps({}).encode('utf-8'))
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        if self.path.startswith('/api/sumulas/'):
            tribunal = self.path.split('/')[-1]
            if tribunal in ['stf', 'stj', 'eca']:
                try:
                    data = json.loads(post_data.decode('utf-8'))
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
        
        elif self.path.startswith('/api/temas/'):
            tribunal = self.path.split('/')[-1]
            if tribunal in ['stf', 'stj']:
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    arquivo = f'Data/temas_{tribunal}.json'
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
        
        elif self.path == '/api/categorias':
            try:
                data = json.loads(post_data.decode('utf-8'))
                arquivo = 'Data/categorias_cores.json'
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
                import locale
                import sys
                system_encoding = locale.getpreferredencoding()
                python_exe = sys.executable
                
                # Gerar ambos os HTMLs
                result_sumulas = subprocess.run(
                    [python_exe, 'Scripts/generators/1_gerar_html_sumulas.py'],
                    capture_output=True,
                    text=True,
                    encoding=system_encoding,
                    errors='replace',
                    timeout=30
                )
                
                result_temas = subprocess.run(
                    [python_exe, 'Scripts/generators/1_gerar_html_temas.py'],
                    capture_output=True,
                    text=True,
                    encoding=system_encoding,
                    errors='replace',
                    timeout=30
                )
                
                success = result_sumulas.returncode == 0 and result_temas.returncode == 0
                output = f"SÚMULAS:\n{result_sumulas.stdout}\n\nTEMAS:\n{result_temas.stdout}"
                error = f"{result_sumulas.stderr}\n{result_temas.stderr}" if not success else ''
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                self.wfile.write(json.dumps({
                    'success': success,
                    'output': output,
                    'error': error
                }, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        
        elif self.path == '/api/git/push':
            try:
                data = json.loads(post_data.decode('utf-8'))
                commit_message = data.get('message', 'Atualização de súmulas e temas')
                
                # Verificar se há mudanças
                result = subprocess.run(
                    ['git', 'status', '--porcelain'],
                    capture_output=True,
                    text=True,
                    cwd=os.getcwd()
                )
                
                if not result.stdout.strip():
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        'success': True,
                        'message': '✓ Não há mudanças para commitar',
                        'hasChanges': False
                    }).encode('utf-8'))
                    return
                
                # Adicionar arquivos
                subprocess.run(['git', 'add', '.'], cwd=os.getcwd(), check=True)
                
                # Commit
                subprocess.run(['git', 'commit', '-m', commit_message], cwd=os.getcwd(), check=True)
                
                # Push
                subprocess.run(['git', 'push'], cwd=os.getcwd(), check=True)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': True,
                    'message': '✓ Mudanças enviadas para o GitHub!',
                    'hasChanges': True,
                    'commitMessage': commit_message
                }).encode('utf-8'))
            except subprocess.CalledProcessError as e:
                error_msg = 'Erro ao executar comando Git'
                if 'nothing to commit' in str(e):
                    error_msg = 'Não há mudanças para commitar'
                elif 'not a git repository' in str(e):
                    error_msg = 'Diretório não é um repositório Git'
                
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': False,
                    'error': error_msg
                }).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': False,
                    'error': str(e)
                }).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        # Suprimir logs HTTP padrão
        pass
    
    def get_html(self):
        return '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Editor Unificado - Súmulas e Temas</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .tab-button {
            transition: all 0.3s ease;
        }
        .tab-button.active {
            border-bottom: 3px solid #3b82f6;
            color: #3b82f6;
        }
        #toast {
            transition: all 0.3s ease;
        }
    </style>
</head>
<body class="bg-gray-50">
    <!-- Toast de Notificação -->
    <div id="toast" class="fixed top-4 right-4 z-50 hidden"></div>

    <!-- Header -->
    <div class="bg-gradient-to-r from-blue-600 to-blue-800 text-white shadow-lg">
        <div class="container mx-auto px-4 py-6">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-3xl font-bold">📝 Editor Unificado</h1>
                    <p class="text-blue-100 mt-1">Súmulas e Temas em uma única interface</p>
                </div>
                <div class="flex gap-3">
                    <button onclick="gerarHTML()" id="btn-gerar"
                        class="px-6 py-3 bg-green-500 hover:bg-green-600 text-white rounded-lg font-semibold shadow-lg flex items-center gap-2 transition">
                        🔄 Gerar HTML
                    </button>
                    <button onclick="gitPush()" id="btn-git"
                        class="px-6 py-3 bg-purple-500 hover:bg-purple-600 text-white rounded-lg font-semibold shadow-lg flex items-center gap-2 transition">
                        🚀 Commit & Push
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Tabs -->
    <div class="bg-white border-b border-gray-200">
        <div class="container mx-auto px-4">
            <div class="flex gap-6">
                <button onclick="mudarAba('sumulas')" id="tab-sumulas" 
                    class="tab-button px-4 py-4 font-semibold text-gray-600 active">
                    📋 SÚMULAS
                </button>
                <button onclick="mudarAba('temas')" id="tab-temas"
                    class="tab-button px-4 py-4 font-semibold text-gray-600">
                    🎯 TEMAS
                </button>
            </div>
        </div>
    </div>

    <!-- Conteúdo -->
    <div class="container mx-auto px-4 py-8">
        <!-- Aba Súmulas -->
        <div id="content-sumulas">
            <iframe src="http://localhost:8001" 
                style="width:100%; height:calc(100vh - 300px); border:none;">
            </iframe>
            <p class="text-sm text-gray-500 mt-4">💡 Editor de Súmulas carregado na porta 8001</p>
        </div>

        <!-- Aba Temas -->
        <div id="content-temas" class="hidden">
            <iframe src="http://localhost:8002" 
                style="width:100%; height:calc(100vh - 300px); border:none;">
            </iframe>
            <p class="text-sm text-gray-500 mt-4">💡 Editor de Temas carregado na porta 8002</p>
        </div>
    </div>

    <script>
        let abaAtual = 'sumulas';

        function mudarAba(aba) {
            abaAtual = aba;
            
            // Atualizar tabs
            document.getElementById('tab-sumulas').classList.toggle('active', aba === 'sumulas');
            document.getElementById('tab-temas').classList.toggle('active', aba === 'temas');
            
            // Atualizar conteúdo
            document.getElementById('content-sumulas').classList.toggle('hidden', aba !== 'sumulas');
            document.getElementById('content-temas').classList.toggle('hidden', aba !== 'temas');
        }

        function mostrarToast(mensagem, tipo = 'success') {
            const toast = document.getElementById('toast');
            const cor = tipo === 'success' ? 'bg-green-500' : 'bg-red-500';
            
            toast.className = `fixed top-4 right-4 z-50 ${cor} text-white px-6 py-3 rounded-lg shadow-lg flex items-center gap-2`;
            toast.innerHTML = tipo === 'success' ? 
                `<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>` :
                `<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                </svg>`;
            toast.innerHTML += `<span>${mensagem}</span>`;
            toast.classList.remove('hidden');
            
            setTimeout(() => {
                toast.classList.add('hidden');
            }, 4000);
        }

        async function gerarHTML() {
            const btn = document.getElementById('btn-gerar');
            btn.disabled = true;
            btn.textContent = '⏳ Gerando...';
            
            try {
                const response = await fetch('/api/gerar-html', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
                
                const data = await response.json();
                
                if (data.success) {
                    mostrarToast('✓ HTML gerado com sucesso!', 'success');
                } else {
                    mostrarToast('Erro: ' + data.error, 'error');
                }
            } catch (error) {
                mostrarToast('Erro ao gerar HTML: ' + error, 'error');
            } finally {
                btn.disabled = false;
                btn.innerHTML = '🔄 Gerar HTML';
            }
        }

        async function gitPush() {
            if (!confirm('Fazer commit e push das mudanças para o GitHub?\\n\\nIsso irá:\\n1. Adicionar todos os arquivos modificados\\n2. Fazer commit\\n3. Fazer push para o repositório')) {
                return;
            }
            
            const btn = document.getElementById('btn-git');
            btn.disabled = true;
            btn.textContent = '⏳ Enviando...';
            
            try {
                const response = await fetch('/api/git/push', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        message: 'Atualização de súmulas e temas - ' + new Date().toLocaleString('pt-BR')
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    if (data.hasChanges) {
                        mostrarToast('✓ Mudanças enviadas para o GitHub!', 'success');
                    } else {
                        mostrarToast('✓ Não há mudanças para commitar', 'success');
                    }
                } else {
                    mostrarToast('Erro: ' + data.error, 'error');
                }
            } catch (error) {
                mostrarToast('Erro ao fazer push: ' + error, 'error');
            } finally {
                btn.disabled = false;
                btn.innerHTML = '🚀 Commit & Push';
            }
        }
    </script>
</body>
</html>'''

def abrir_navegador():
    webbrowser.open('http://localhost:8000')

if __name__ == '__main__':
    PORT = 8000
    print("\n" + "="*80)
    print("🎯 EDITOR UNIFICADO - SÚMULAS E TEMAS")
    print("="*80)
    print()
    print(f"✓ Servidor principal: http://localhost:{PORT}")
    print("✓ Editor de Súmulas:  http://localhost:8001")
    print("✓ Editor de Temas:    http://localhost:8002")
    print()
    print("💡 INSTRUÇÕES:")
    print("   1. Execute simultaneamente:")
    print("      - python Scripts/editors/2_servidor_sumulas.py     (porta 8001)")
    print("      - python Scripts/editors/2_servidor_temas.py (porta 8002)")
    print("      - python Scripts/editors/3_servidor_unificado.py    (porta 8000)")
    print()
    print("   2. Ou use o arquivo .bat para iniciar tudo automaticamente")
    print()
    print("🚀 RECURSOS:")
    print("   - Alternar entre Súmulas e Temas em abas")
    print("   - Gerar HTML de ambos com um clique")
    print("   - Commit & Push Git direto do editor")
    print()
    print("="*80)
    print()
    
    # Abrir navegador após 2 segundos
    Timer(2, abrir_navegador).start()
    
    try:
        server = HTTPServer(('localhost', PORT), EditorHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✓ Servidor encerrado")
        server.socket.close()
