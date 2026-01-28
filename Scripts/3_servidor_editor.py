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
        
        elif self.path == '/config':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(self.get_config_html().encode('utf-8'))
            
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
        
        elif self.path == '/api/categorias':
            try:
                data = json.loads(post_data.decode('utf-8'))
                
                # Salvar categorias
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
    
    def get_config_html(self):
        return '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Configurar Categorias - ResumosDireito</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
    <div class="container mx-auto px-4 py-8 max-w-4xl">
        <div class="mb-6">
            <a href="/" class="text-blue-600 hover:text-blue-800">← Voltar ao Editor</a>
        </div>
        
        <header class="text-center mb-8">
            <h1 class="text-4xl font-bold text-blue-900 mb-2">⚙️ Configurar Categorias</h1>
            <p class="text-gray-600">Edite o nome das categorias para cada cor</p>
        </header>

        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
            <form id="form-categorias" class="space-y-4">
                <div id="lista-cores"></div>
                
                <div class="flex gap-4 pt-4">
                    <button type="submit" class="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold">
                        💾 Salvar Configurações
                    </button>
                    <button type="button" onclick="resetarPadrao()" class="px-6 py-3 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 font-semibold">
                        🔄 Restaurar Padrão
                    </button>
                </div>
            </form>
        </div>

        <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 class="font-bold text-blue-900 mb-2">💡 Dica:</h3>
            <p class="text-sm text-blue-800">Após salvar, reinicie o editor para ver as alterações no dropdown de cores!</p>
        </div>
    </div>

    <script>
        const coresEmoji = {
            red: '#ef4444', orange: '#f97316', green: '#22c55e', teal: '#14b8a6', indigo: '#6366f1',
            purple: '#a855f7', pink: '#ec4899', rose: '#f43f5e', blue: '#3b82f6', cyan: '#06b6d4',
            lime: '#84cc16', amber: '#f59e0b', emerald: '#10b981', violet: '#8b5cf6', fuchsia: '#d946ef',
            magenta: '#e11d48', yellow: '#eab308', brown: '#92400e', coral: '#fb7185', stone: '#78716c', gray: '#6b7280'
        };
        
        const coresNome = {
            red: 'Vermelho', orange: 'Laranja', green: 'Verde', teal: 'Teal', indigo: 'Índigo',
            purple: 'Roxo', pink: 'Rosa', rose: 'Rosa-forte', blue: 'Azul', cyan: 'Ciano',
            lime: 'Lima', amber: 'Âmbar', emerald: 'Esmeralda', violet: 'Violeta', fuchsia: 'Fúcsia',
            magenta: 'Magenta', yellow: 'Amarelo', brown: 'Marrom', coral: 'Coral', stone: 'Pedra', gray: 'Cinza'
        };

        let categorias = {};

        async function carregarCategorias() {
            try {
                const response = await fetch('/api/categorias');
                categorias = await response.json();
                renderizarLista();
            } catch (error) {
                mostrarToast('Erro ao carregar categorias', 'error');
            }
        }

        function renderizarLista() {
            const lista = document.getElementById('lista-cores');
            lista.innerHTML = Object.keys(coresNome).map(cor => `
                <div class="flex items-center gap-4 p-3 border rounded-lg hover:bg-gray-50">
                    <div class="flex items-center gap-2 w-48">
                        <span class="inline-block w-6 h-6 rounded-full" style="background-color: ${coresEmoji[cor]}"></span>
                        <span class="font-medium text-gray-700">${coresNome[cor]}</span>
                    </div>
                    <input type="text" 
                           data-cor="${cor}"
                           value="${categorias[cor] || ''}"
                           placeholder="Nome da categoria"
                           class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                </div>
            `).join('');
        }

        document.getElementById('form-categorias').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const inputs = document.querySelectorAll('[data-cor]');
            const novasCategorias = {};
            
            inputs.forEach(input => {
                const cor = input.getAttribute('data-cor');
                const valor = input.value.trim();
                if (valor) {
                    novasCategorias[cor] = valor;
                }
            });
            
            try {
                const response = await fetch('/api/categorias', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(novasCategorias)
                });
                
                if (response.ok) {
                    mostrarToast('✓ Configurações salvas com sucesso!', 'success');
                    categorias = novasCategorias;
                } else {
                    mostrarToast('Erro ao salvar configurações', 'error');
                }
            } catch (error) {
                mostrarToast('Erro ao salvar configurações', 'error');
            }
        });

        function resetarPadrao() {
            if (!confirm('Deseja restaurar as categorias padrão?')) return;
            
            const padrao = {
                red: 'Júri', orange: 'Execução Penal', green: 'Crimes Geral',
                teal: 'Processual', indigo: 'Prescrição', purple: 'Competência',
                pink: 'Aplicação da Pena', rose: 'Perdão Judicial', blue: 'Outros',
                cyan: 'Recursos', lime: 'Ação Penal', amber: 'Medidas Cautelares',
                emerald: 'Crimes Contra Ordem', violet: 'Nulidades',
                fuchsia: 'Suspensão Condicional', sky: 'Garantias', yellow: 'Prova',
                slate: 'Especial', zinc: 'Transação', stone: 'Crimes Tributários', gray: 'Diversos'
            };
            
            categorias = padrao;
            renderizarLista();
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

        carregarCategorias();
    </script>
</body>
</html>'''
    
    def get_html(self):
        return '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Editor de Súmulas - ResumosDireito</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        magenta: {
                            50: '#fdf2f8',
                            100: '#fce7f3',
                            200: '#fbcfe8',
                            300: '#f9a8d4',
                            400: '#f472b6',
                            500: '#e11d48',
                            600: '#be123c',
                            700: '#9f1239',
                            800: '#881337',
                            900: '#701a2e'
                        },
                        coral: {
                            50: '#fff1f2',
                            100: '#ffe4e6',
                            200: '#fecdd3',
                            300: '#fda4af',
                            400: '#fb7185',
                            500: '#fb7185',
                            600: '#f43f5e',
                            700: '#e11d48',
                            800: '#be123c',
                            900: '#9f1239'
                        },
                        brown: {
                            50: '#fefce8',
                            100: '#fef9c3',
                            200: '#fef08a',
                            300: '#fde047',
                            400: '#facc15',
                            500: '#92400e',
                            600: '#78350f',
                            700: '#78350f',
                            800: '#451a03',
                            900: '#451a03'
                        }
                    }
                }
            }
        }
    </script>
    <style>
        .sumula-item {
            transition: all 0.2s;
        }
        .sumula-item:hover {
            transform: translateX(4px);
        }
        .line-clamp-2 {
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        /* Indicador de cor customizado */
        .cor-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
            vertical-align: middle;
        }
    </style>
</head>
<body class="bg-gray-50">
    <div class="container mx-auto px-4 py-8 max-w-7xl">
        <div class="flex justify-end mb-4">
            <a href="/config" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition font-medium">
                ⚙️ Configurar Categorias
            </a>
        </div>
        
        <header class="text-center mb-8">
            <h1 class="text-4xl font-bold text-blue-900 mb-2">📝 Editor de Súmulas</h1>
            <p class="text-gray-600">Edição direta com salvamento automático</p>
        </header>

        <!-- Seletor de Tribunal -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-8">
            <div class="flex gap-4 mb-4">
                <button onclick="selecionarTribunal('todos')" id="btn-todos"
                    class="flex-1 px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition font-semibold">
                    TODOS (<span id="count-todos">0</span>)
                </button>
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
                
                <!-- Barra de Pesquisa -->
                <div class="mb-4">
                    <div class="relative mb-2">
                        <input type="text" id="pesquisa-sumulas" 
                            placeholder="🔍 Pesquisar no texto das súmulas..."
                            class="w-full px-4 py-2 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        <button onclick="limparPesquisa()" 
                            class="absolute right-2 top-2 text-gray-400 hover:text-gray-600">
                            ✖
                        </button>
                    </div>
                    
                    <!-- Filtro por Cor -->
                    <div class="flex flex-wrap gap-1 mb-2" id="filtro-cores">
                        <!-- Preenchido dinamicamente -->
                    </div>
                    
                    <div id="resultado-pesquisa" class="text-sm text-gray-600"></div>
                </div>
                
                <!-- Ações em Massa -->
                <div id="acoes-massa" class="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg hidden">
                    <div class="flex items-center justify-between mb-2">
                        <span class="text-sm font-medium text-blue-900">
                            <span id="count-selecionadas">0</span> selecionadas
                        </span>
                        <button onclick="desmarcarTodas()" class="text-xs text-blue-600 hover:text-blue-800">
                            Desmarcar todas
                        </button>
                    </div>
                    <div class="flex gap-2">
                        <div class="relative flex-1">
                            <button type="button" id="cor-massa-button" 
                                class="w-full px-3 py-2 text-sm border border-blue-300 rounded-lg bg-white text-left flex items-center justify-between">
                                <span id="cor-massa-selected" class="flex items-center">
                                    <span>Selecione uma cor...</span>
                                </span>
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                                </svg>
                            </button>
                            <input type="hidden" id="cor-massa" value="">
                            <div id="cor-massa-dropdown" class="hidden absolute z-20 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-auto">
                                <!-- Preenchido dinamicamente -->
                            </div>
                        </div>
                        <button onclick="aplicarCorEmMassa()" 
                            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-semibold">
                            🎨 Aplicar
                        </button>
                    </div>
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
                    <p class="text-xs mt-4 text-blue-600 hidden" id="aviso-todos">💡 Selecione um tribunal específico para adicionar novas súmulas</p>
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
                            <div class="relative">
                                <button type="button" id="cor-button" 
                                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 bg-white text-left flex items-center justify-between">
                                    <span id="cor-selected" class="flex items-center">
                                        <span class="cor-indicator bg-blue-500"></span>
                                        <span>Azul - Outros</span>
                                    </span>
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                                    </svg>
                                </button>
                                <input type="hidden" id="cor" value="blue">
                                <div id="cor-dropdown" class="hidden absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-auto">
                                    <!-- Preenchido dinamicamente -->
                                </div>
                            </div>
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
                        <label class="block text-sm font-medium text-gray-700 mb-2">Modulação de Efeitos</label>
                        <textarea id="modulacao_efeitos" rows="3"
                            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                            placeholder="Informações sobre modulação de efeitos (se houver)"></textarea>
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
        let tribunalAtual = 'todos';
        let sumulas = [];
        let todasSumulas = {}; // Armazena todas as súmulas de todos os tribunais
        let categorias = {};
        let sumulasSelecionadas = new Set();
        let textoPesquisa = '';
        let coresFiltradas = new Set(); // Cores selecionadas para filtro

        // Carregar categorias
        async function carregarCategorias() {
            try {
                const response = await fetch('/api/categorias');
                categorias = await response.json();
                atualizarDropdownCores();
                atualizarDropdownCoreMassa();
                criarFiltroCores(); // Criar filtro após carregar categorias
            } catch (error) {
                console.error('Erro ao carregar categorias:', error);
            }
        }

        function atualizarDropdownCoreMassa() {
            const button = document.getElementById('cor-massa-button');
            const dropdown = document.getElementById('cor-massa-dropdown');
            const corInput = document.getElementById('cor-massa');
            const corSelected = document.getElementById('cor-massa-selected');
            
            if (!button || !dropdown) return;
            
            const coresConfig = [
                {cor: 'red', nome: 'Vermelho', hex: '#ef4444'},
                {cor: 'orange', nome: 'Laranja', hex: '#f97316'},
                {cor: 'green', nome: 'Verde', hex: '#22c55e'},
                {cor: 'teal', nome: 'Teal', hex: '#14b8a6'},
                {cor: 'indigo', nome: 'Índigo', hex: '#6366f1'},
                {cor: 'purple', nome: 'Roxo', hex: '#a855f7'},
                {cor: 'pink', nome: 'Rosa', hex: '#ec4899'},
                {cor: 'rose', nome: 'Rosa-forte', hex: '#f43f5e'},
                {cor: 'blue', nome: 'Azul', hex: '#3b82f6'},
                {cor: 'cyan', nome: 'Ciano', hex: '#06b6d4'},
                {cor: 'lime', nome: 'Lima', hex: '#84cc16'},
                {cor: 'amber', nome: 'Âmbar', hex: '#f59e0b'},
                {cor: 'emerald', nome: 'Esmeralda', hex: '#10b981'},
                {cor: 'violet', nome: 'Violeta', hex: '#8b5cf6'},
                {cor: 'fuchsia', nome: 'Fúcsia', hex: '#d946ef'},
                {cor: 'magenta', nome: 'Magenta', hex: '#e11d48'},
                {cor: 'yellow', nome: 'Amarelo', hex: '#eab308'},
                {cor: 'brown', nome: 'Marrom', hex: '#92400e'},
                {cor: 'coral', nome: 'Coral', hex: '#fb7185'},
                {cor: 'stone', nome: 'Pedra', hex: '#78716c'},
                {cor: 'gray', nome: 'Cinza', hex: '#6b7280'}
            ];
            
            // Preencher dropdown
            dropdown.innerHTML = coresConfig.map(c => {
                const categoria = categorias[c.cor] || '';
                const texto = categoria ? `${c.nome} - ${categoria}` : c.nome;
                return `
                    <div class="px-4 py-2 hover:bg-gray-100 cursor-pointer flex items-center text-sm" 
                         data-cor="${c.cor}" data-nome="${texto}" data-hex="${c.hex}">
                        <span class="cor-indicator" style="background-color: ${c.hex}"></span>
                        <span>${texto}</span>
                    </div>
                `;
            }).join('');
            
            // Toggle dropdown
            button.onclick = (e) => {
                e.preventDefault();
                dropdown.classList.toggle('hidden');
            };
            
            // Fechar ao clicar fora
            document.addEventListener('click', (e) => {
                if (!button.contains(e.target) && !dropdown.contains(e.target)) {
                    dropdown.classList.add('hidden');
                }
            });
            
            // Selecionar cor
            dropdown.querySelectorAll('[data-cor]').forEach(item => {
                item.onclick = () => {
                    const cor = item.dataset.cor;
                    const nome = item.dataset.nome;
                    const hex = item.dataset.hex;
                    
                    corInput.value = cor;
                    corSelected.innerHTML = `
                        <span class="cor-indicator" style="background-color: ${hex}"></span>
                        <span>${nome}</span>
                    `;
                    dropdown.classList.add('hidden');
                };
            });
        }

        function atualizarDropdownCores() {
            const button = document.getElementById('cor-button');
            const dropdown = document.getElementById('cor-dropdown');
            const corInput = document.getElementById('cor');
            const corSelected = document.getElementById('cor-selected');
            
            if (!button || !dropdown) return;
            
            const coresConfig = [
                {cor: 'red', nome: 'Vermelho', hex: '#ef4444'},
                {cor: 'orange', nome: 'Laranja', hex: '#f97316'},
                {cor: 'green', nome: 'Verde', hex: '#22c55e'},
                {cor: 'teal', nome: 'Teal', hex: '#14b8a6'},
                {cor: 'indigo', nome: 'Índigo', hex: '#6366f1'},
                {cor: 'purple', nome: 'Roxo', hex: '#a855f7'},
                {cor: 'pink', nome: 'Rosa', hex: '#ec4899'},
                {cor: 'rose', nome: 'Rosa-forte', hex: '#f43f5e'},
                {cor: 'blue', nome: 'Azul', hex: '#3b82f6'},
                {cor: 'cyan', nome: 'Ciano', hex: '#06b6d4'},
                {cor: 'lime', nome: 'Lima', hex: '#84cc16'},
                {cor: 'amber', nome: 'Âmbar', hex: '#f59e0b'},
                {cor: 'emerald', nome: 'Esmeralda', hex: '#10b981'},
                {cor: 'violet', nome: 'Violeta', hex: '#8b5cf6'},
                {cor: 'fuchsia', nome: 'Fúcsia', hex: '#d946ef'},
                {cor: 'magenta', nome: 'Magenta', hex: '#e11d48'},
                {cor: 'yellow', nome: 'Amarelo', hex: '#eab308'},
                {cor: 'brown', nome: 'Marrom', hex: '#92400e'},
                {cor: 'coral', nome: 'Coral', hex: '#fb7185'},
                {cor: 'stone', nome: 'Pedra', hex: '#78716c'},
                {cor: 'gray', nome: 'Cinza', hex: '#6b7280'}
            ];
            
            // Preencher dropdown
            dropdown.innerHTML = coresConfig.map(c => {
                const categoria = categorias[c.cor] || '';
                const texto = categoria ? `${c.nome} - ${categoria}` : c.nome;
                return `
                    <div class="px-4 py-2 hover:bg-gray-100 cursor-pointer flex items-center" 
                         data-cor="${c.cor}" data-nome="${texto}" data-hex="${c.hex}">
                        <span class="cor-indicator" style="background-color: ${c.hex}"></span>
                        <span>${texto}</span>
                    </div>
                `;
            }).join('');
            
            // Toggle dropdown
            button.onclick = (e) => {
                e.preventDefault();
                dropdown.classList.toggle('hidden');
            };
            
            // Fechar ao clicar fora
            document.addEventListener('click', (e) => {
                if (!button.contains(e.target) && !dropdown.contains(e.target)) {
                    dropdown.classList.add('hidden');
                }
            });
            
            // Selecionar cor
            dropdown.querySelectorAll('[data-cor]').forEach(item => {
                item.onclick = () => {
                    const cor = item.dataset.cor;
                    const nome = item.dataset.nome;
                    const hex = item.dataset.hex;
                    
                    corInput.value = cor;
                    corSelected.innerHTML = `
                        <span class="cor-indicator" style="background-color: ${hex}"></span>
                        <span>${nome}</span>
                    `;
                    dropdown.classList.add('hidden');
                };
            });
        }

        async function carregarSumulas(tribunal) {
            try {
                if (tribunal === 'todos') {
                    // Carregar todos os tribunais
                    const [stfRes, stjRes, ecaRes] = await Promise.all([
                        fetch('/api/sumulas/stf'),
                        fetch('/api/sumulas/stj'),
                        fetch('/api/sumulas/eca')
                    ]);
                    
                    const [stfData, stjData, ecaData] = await Promise.all([
                        stfRes.json(),
                        stjRes.json(),
                        ecaRes.json()
                    ]);
                    
                    todasSumulas = {
                        stf: stfData.sumulas || [],
                        stj: stjData.sumulas || [],
                        eca: ecaData.sumulas || []
                    };
                    
                    // Combinar todas com identificação do tribunal
                    sumulas = [
                        ...todasSumulas.stf.map(s => ({...s, _tribunal: 'STF'})),
                        ...todasSumulas.stj.map(s => ({...s, _tribunal: 'STJ'})),
                        ...todasSumulas.eca.map(s => ({...s, _tribunal: 'ECA'}))
                    ].sort((a, b) => a.numero - b.numero);
                    
                } else {
                    const response = await fetch(`/api/sumulas/${tribunal}`);
                    const data = await response.json();
                    todasSumulas[tribunal] = data.sumulas || [];
                    sumulas = todasSumulas[tribunal].map(s => ({...s, _tribunal: tribunal.toUpperCase()}));
                }
                
                atualizarLista();
                atualizarContador();
                criarFiltroCores(); // Atualizar filtro de cores após carregar súmulas
            } catch (error) {
                mostrarToast('Erro ao carregar súmulas', 'error');
            }
        }

        function atualizarLista() {
            const lista = document.getElementById('lista-sumulas');
            
            // Filtrar súmulas pela pesquisa e por cor
            let sumulasFiltradas = sumulas;
            
            // Filtro de texto
            if (textoPesquisa) {
                const termo = textoPesquisa.toLowerCase();
                sumulasFiltradas = sumulasFiltradas.filter(s => 
                    s.texto.toLowerCase().includes(termo) ||
                    s.titulo.toLowerCase().includes(termo) ||
                    s.numero.toString().includes(termo)
                );
            }
            
            // Filtro de cores
            if (coresFiltradas.size > 0) {
                sumulasFiltradas = sumulasFiltradas.filter(s => coresFiltradas.has(s.cor));
            }
            
            // Atualizar contador de resultados
            const resultadoDiv = document.getElementById('resultado-pesquisa');
            if (textoPesquisa || coresFiltradas.size > 0) {
                resultadoDiv.textContent = `${sumulasFiltradas.length} de ${sumulas.length} súmulas`;
            } else {
                resultadoDiv.textContent = '';
            }
            
            if (sumulasFiltradas.length === 0) {
                lista.innerHTML = '<p class="text-gray-500 text-center py-8">Nenhuma súmula encontrada</p>';
                return;
            }

            lista.innerHTML = sumulasFiltradas.map((s, i) => {
                // Encontrar índice original
                const indiceOriginal = sumulas.indexOf(s);
                const selecionada = sumulasSelecionadas.has(indiceOriginal);
                const borderClass = selecionada ? 'border-blue-500 bg-blue-50' : 'border-gray-300';
                
                // Badge do tribunal (só mostra quando está em "TODOS")
                const badgeTribunal = tribunalAtual === 'todos' ? 
                    `<span class="px-2 py-1 text-xs font-bold rounded ${
                        s._tribunal === 'STF' ? 'bg-red-100 text-red-700' :
                        s._tribunal === 'STJ' ? 'bg-indigo-100 text-indigo-700' :
                        'bg-purple-100 text-purple-700'
                    }">${s._tribunal}</span>` : '';
                
                return `
                <div class="sumula-item p-3 border ${borderClass} rounded-lg cursor-pointer hover:bg-gray-50 hover:border-blue-400 relative">
                    <div class="flex items-start gap-2">
                        <input type="checkbox" 
                               ${selecionada ? 'checked' : ''}
                               onchange="toggleSelecionada(${indiceOriginal})"
                               onclick="event.stopPropagation()"
                               class="mt-1 w-4 h-4 text-blue-600 rounded">
                        <div onclick="editarSumula(${indiceOriginal})" class="flex-1">
                            <div class="flex items-center justify-between gap-2">
                                <div class="flex items-center gap-2 flex-wrap">
                                    ${badgeTribunal}
                                    <span class="font-bold text-lg">${s.numero}</span>
                                    <span class="text-gray-700">${s.titulo}</span>
                                </div>
                                <div class="w-4 h-4 rounded-full bg-${s.cor}-500 flex-shrink-0"></div>
                            </div>
                            ${textoPesquisa ? `<p class="text-xs text-gray-600 mt-1 line-clamp-2">${s.texto}</p>` : ''}
                        </div>
                    </div>
                </div>
            `}).join('');
            
            atualizarAcoesMassa();
        }

        function toggleSelecionada(indice) {
            if (sumulasSelecionadas.has(indice)) {
                sumulasSelecionadas.delete(indice);
            } else {
                sumulasSelecionadas.add(indice);
            }
            atualizarLista();
        }

        function desmarcarTodas() {
            sumulasSelecionadas.clear();
            atualizarLista();
        }

        function atualizarAcoesMassa() {
            const acoesMassa = document.getElementById('acoes-massa');
            const count = document.getElementById('count-selecionadas');
            
            count.textContent = sumulasSelecionadas.size;
            
            if (sumulasSelecionadas.size > 0) {
                acoesMassa.classList.remove('hidden');
            } else {
                acoesMassa.classList.add('hidden');
            }
        }

        async function aplicarCorEmMassa() {
            const corSelecionada = document.getElementById('cor-massa').value;
            
            if (!corSelecionada) {
                mostrarToast('Selecione uma cor', 'error');
                return;
            }
            
            if (sumulasSelecionadas.size === 0) {
                mostrarToast('Selecione pelo menos uma súmula', 'error');
                return;
            }
            
            const quantidade = sumulasSelecionadas.size;
            
            if (!confirm(`Alterar cor de ${quantidade} súmula(s)?`)) {
                return;
            }
            
            // Aplicar cor nas súmulas selecionadas
            sumulasSelecionadas.forEach(indice => {
                sumulas[indice].cor = corSelecionada;
            });
            
            // Salvar - precisa separar por tribunal no modo TODOS
            if (tribunalAtual === 'todos') {
                // Reorganizar súmulas por tribunal
                const porTribunal = { stf: [], stj: [], eca: [] };
                
                sumulas.forEach(s => {
                    const trib = s._tribunal.toLowerCase();
                    // Criar cópia sem _tribunal
                    const { _tribunal, ...sumulaLimpa } = s;
                    porTribunal[trib].push(sumulaLimpa);
                });
                
                // Salvar cada tribunal
                try {
                    await Promise.all([
                        salvarTribunal('stf', porTribunal.stf),
                        salvarTribunal('stj', porTribunal.stj),
                        salvarTribunal('eca', porTribunal.eca)
                    ]);
                    
                    mostrarToast(`✓ Cor alterada em ${quantidade} súmula(s)!`, 'success');
                    
                    // Recarregar
                    await carregarSumulas('todos');
                } catch (error) {
                    mostrarToast('Erro ao salvar', 'error');
                }
            } else {
                // Modo normal - salvar só o tribunal atual
                await salvarSumula();
                mostrarToast(`✓ Cor alterada em ${quantidade} súmula(s)!`, 'success');
            }
            
            // Limpar seleção
            sumulasSelecionadas.clear();
            atualizarLista();
        }
        
        async function salvarTribunal(tribunal, sumulasArray) {
            const data = {
                tribunal: tribunal.toUpperCase(),
                total: sumulasArray.length,
                sumulas: sumulasArray
            };
            
            const response = await fetch(`/api/sumulas/${tribunal}`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                throw new Error(`Erro ao salvar ${tribunal}`);
            }
        }

        // Pesquisa
        document.addEventListener('DOMContentLoaded', () => {
            const inputPesquisa = document.getElementById('pesquisa-sumulas');
            if (inputPesquisa) {
                inputPesquisa.addEventListener('input', (e) => {
                    textoPesquisa = e.target.value;
                    atualizarLista();
                });
            }
        });

        function limparPesquisa() {
            const inputPesquisa = document.getElementById('pesquisa-sumulas');
            if (inputPesquisa) {
                inputPesquisa.value = '';
                textoPesquisa = '';
                atualizarLista();
            }
        }
        
        function criarFiltroCores() {
            const filtroCores = document.getElementById('filtro-cores');
            if (!filtroCores) return;
            
            // Contar quantas súmulas de cada cor existem
            const coresUsadas = new Map();
            sumulas.forEach(s => {
                coresUsadas.set(s.cor, (coresUsadas.get(s.cor) || 0) + 1);
            });
            
            const coresConfig = [
                {cor: 'red', nome: 'Vermelho', hex: '#ef4444'},
                {cor: 'orange', nome: 'Laranja', hex: '#f97316'},
                {cor: 'green', nome: 'Verde', hex: '#22c55e'},
                {cor: 'teal', nome: 'Teal', hex: '#14b8a6'},
                {cor: 'indigo', nome: 'Índigo', hex: '#6366f1'},
                {cor: 'purple', nome: 'Roxo', hex: '#a855f7'},
                {cor: 'pink', nome: 'Rosa', hex: '#ec4899'},
                {cor: 'rose', nome: 'Rosa-forte', hex: '#f43f5e'},
                {cor: 'blue', nome: 'Azul', hex: '#3b82f6'},
                {cor: 'cyan', nome: 'Ciano', hex: '#06b6d4'},
                {cor: 'lime', nome: 'Lima', hex: '#84cc16'},
                {cor: 'amber', nome: 'Âmbar', hex: '#f59e0b'},
                {cor: 'emerald', nome: 'Esmeralda', hex: '#10b981'},
                {cor: 'violet', nome: 'Violeta', hex: '#8b5cf6'},
                {cor: 'fuchsia', nome: 'Fúcsia', hex: '#d946ef'},
                {cor: 'magenta', nome: 'Magenta', hex: '#e11d48'},
                {cor: 'yellow', nome: 'Amarelo', hex: '#eab308'},
                {cor: 'brown', nome: 'Marrom', hex: '#92400e'},
                {cor: 'coral', nome: 'Coral', hex: '#fb7185'},
                {cor: 'stone', nome: 'Pedra', hex: '#78716c'},
                {cor: 'gray', nome: 'Cinza', hex: '#6b7280'}
            ];
            
            // Filtrar apenas cores que estão sendo usadas
            const coresComSumulas = coresConfig.filter(c => coresUsadas.has(c.cor));
            
            filtroCores.innerHTML = `
                <button onclick="limparFiltros()" 
                    class="px-3 py-1.5 text-xs bg-gray-100 hover:bg-gray-200 rounded border border-gray-300 font-medium">
                    Todas
                </button>
            ` + coresComSumulas.map(c => {
                const categoria = categorias[c.cor] || c.nome;
                const quantidade = coresUsadas.get(c.cor);
                return `
                    <button onclick="toggleFiltroCor('${c.cor}')" 
                        id="filtro-${c.cor}"
                        class="w-8 h-8 bg-white hover:bg-gray-50 rounded border border-gray-300 flex items-center justify-center"
                        title="${categoria} (${quantidade})">
                        <span class="w-5 h-5 rounded-full" style="background-color: ${c.hex};"></span>
                    </button>
                `;
            }).join('');
        }
        
        function toggleFiltroCor(cor) {
            if (coresFiltradas.has(cor)) {
                coresFiltradas.delete(cor);
            } else {
                coresFiltradas.add(cor);
            }
            
            // Atualizar visual dos botões
            const btn = document.getElementById(`filtro-${cor}`);
            if (coresFiltradas.has(cor)) {
                btn.classList.remove('bg-white', 'hover:bg-gray-50');
                btn.classList.add('bg-blue-100', 'border-blue-500', 'ring-2', 'ring-blue-300');
            } else {
                btn.classList.add('bg-white', 'hover:bg-gray-50');
                btn.classList.remove('bg-blue-100', 'border-blue-500', 'ring-2', 'ring-blue-300');
            }
            
            atualizarLista();
        }
        
        function limparFiltros() {
            coresFiltradas.clear();
            
            // Remover destaque de todos os botões
            document.querySelectorAll('[id^="filtro-"]').forEach(btn => {
                btn.classList.add('bg-white', 'hover:bg-gray-50');
                btn.classList.remove('bg-blue-100', 'border-blue-500', 'ring-2', 'ring-blue-300');
            });
            
            atualizarLista();
        }

        async function atualizarContador() {
            for (const tribunal of ['stf', 'stj', 'eca']) {
                const response = await fetch(`/api/sumulas/${tribunal}`);
                const data = await response.json();
                document.getElementById(`count-${tribunal}`).textContent = (data.sumulas || []).length;
            }
            
            // Atualizar contador de todos
            const totalStf = parseInt(document.getElementById('count-stf').textContent) || 0;
            const totalStj = parseInt(document.getElementById('count-stj').textContent) || 0;
            const totalEca = parseInt(document.getElementById('count-eca').textContent) || 0;
            document.getElementById('count-todos').textContent = totalStf + totalStj + totalEca;
        }

        function selecionarTribunal(tribunal) {
            tribunalAtual = tribunal;
            ['todos', 'stf', 'stj', 'eca'].forEach(t => {
                const btn = document.getElementById(`btn-${t}`);
                btn.classList.toggle('ring-4', t === tribunal);
                btn.classList.toggle('ring-offset-2', t === tribunal);
            });
            
            // Atualizar aviso (só para adicionar nova)
            const avisoTodos = document.getElementById('aviso-todos');
            if (avisoTodos) {
                if (tribunal === 'todos') {
                    avisoTodos.classList.remove('hidden');
                } else {
                    avisoTodos.classList.add('hidden');
                }
            }
            
            carregarSumulas(tribunal);
            cancelarEdicao();
            sumulasSelecionadas.clear();
        }

        function novaSumula() {
            if (tribunalAtual === 'todos') {
                mostrarToast('Selecione um tribunal específico para adicionar súmula', 'error');
                return;
            }
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
            document.getElementById('vinculante').checked = sumula.vinculante || false;
            document.getElementById('modulacao_efeitos').value = sumula.modulacao_efeitos || '';
            document.getElementById('nota').value = sumula.nota || '';
            
            // Atualizar dropdown de cor customizado
            const corInput = document.getElementById('cor');
            const corSelected = document.getElementById('cor-selected');
            const corAtual = sumula.cor || 'blue';
            
            corInput.value = corAtual;
            
            // Encontrar informações da cor
            const coresConfig = [
                {cor: 'red', nome: 'Vermelho', hex: '#ef4444'},
                {cor: 'orange', nome: 'Laranja', hex: '#f97316'},
                {cor: 'green', nome: 'Verde', hex: '#22c55e'},
                {cor: 'teal', nome: 'Teal', hex: '#14b8a6'},
                {cor: 'indigo', nome: 'Índigo', hex: '#6366f1'},
                {cor: 'purple', nome: 'Roxo', hex: '#a855f7'},
                {cor: 'pink', nome: 'Rosa', hex: '#ec4899'},
                {cor: 'rose', nome: 'Rosa-forte', hex: '#f43f5e'},
                {cor: 'blue', nome: 'Azul', hex: '#3b82f6'},
                {cor: 'cyan', nome: 'Ciano', hex: '#06b6d4'},
                {cor: 'lime', nome: 'Lima', hex: '#84cc16'},
                {cor: 'amber', nome: 'Âmbar', hex: '#f59e0b'},
                {cor: 'emerald', nome: 'Esmeralda', hex: '#10b981'},
                {cor: 'violet', nome: 'Violeta', hex: '#8b5cf6'},
                {cor: 'fuchsia', nome: 'Fúcsia', hex: '#d946ef'},
                {cor: 'magenta', nome: 'Magenta', hex: '#e11d48'},
                {cor: 'yellow', nome: 'Amarelo', hex: '#eab308'},
                {cor: 'brown', nome: 'Marrom', hex: '#92400e'},
                {cor: 'coral', nome: 'Coral', hex: '#fb7185'},
                {cor: 'stone', nome: 'Pedra', hex: '#78716c'},
                {cor: 'gray', nome: 'Cinza', hex: '#6b7280'}
            ];
            
            const corInfo = coresConfig.find(c => c.cor === corAtual) || coresConfig.find(c => c.cor === 'blue');
            const categoria = categorias[corAtual] || '';
            const textoFinal = categoria ? `${corInfo.nome} - ${categoria}` : corInfo.nome;
            
            if (corSelected) {
                corSelected.innerHTML = `
                    <span class="cor-indicator" style="background-color: ${corInfo.hex}"></span>
                    <span>${textoFinal}</span>
                `;
            }
            
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
                if (tribunalAtual === 'todos') {
                    // Salvar em todos os tribunais
                    const porTribunal = { stf: [], stj: [], eca: [] };
                    
                    sumulas.forEach(s => {
                        if (!s._tribunal) {
                            console.error('Súmula sem tribunal:', s);
                            return;
                        }
                        const trib = s._tribunal.toLowerCase();
                        const { _tribunal, ...sumulaLimpa } = s;
                        porTribunal[trib].push(sumulaLimpa);
                    });
                    
                    await Promise.all([
                        salvarTribunal('stf', porTribunal.stf),
                        salvarTribunal('stj', porTribunal.stj),
                        salvarTribunal('eca', porTribunal.eca)
                    ]);
                } else {
                    // Salvar tribunal específico
                    const sumulasLimpas = sumulas.map(s => {
                        const { _tribunal, ...sumulaLimpa } = s;
                        return sumulaLimpa;
                    });
                    
                    const data = {
                        tribunal: tribunalAtual.toUpperCase(),
                        total: sumulasLimpas.length,
                        sumulas: sumulasLimpas
                    };
                    
                    const response = await fetch(`/api/sumulas/${tribunalAtual}`, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(data)
                    });
                    
                    if (!response.ok) {
                        throw new Error('Erro ao salvar');
                    }
                }
                
                mostrarToast('✓ Salvo com sucesso!', 'success');
                await carregarSumulas(tribunalAtual);
                cancelarEdicao();
            } catch (error) {
                console.error('Erro ao salvar:', error);
                mostrarToast('Erro ao salvar: ' + error.message, 'error');
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
            
            const modulacao_efeitos = document.getElementById('modulacao_efeitos').value;
            if (modulacao_efeitos) sumula.modulacao_efeitos = modulacao_efeitos;
            
            const nota = document.getElementById('nota').value;
            if (nota) sumula.nota = nota;
            
            const indice = document.getElementById('indice-edicao').value;
            if (indice === '') {
                // Adicionar nova
                if (tribunalAtual === 'todos') {
                    mostrarToast('Selecione um tribunal específico para adicionar', 'error');
                    return;
                }
                sumulas.push(sumula);
            } else {
                // Editar existente - preservar _tribunal se existir
                const indiceInt = parseInt(indice);
                const tribunalOriginal = sumulas[indiceInt]._tribunal;
                sumulas[indiceInt] = sumula;
                if (tribunalOriginal) {
                    sumulas[indiceInt]._tribunal = tribunalOriginal;
                }
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
        carregarCategorias(); // Isso já vai chamar criarFiltroCores() depois
        selecionarTribunal('todos');
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
