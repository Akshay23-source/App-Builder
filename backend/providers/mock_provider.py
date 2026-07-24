import json
from typing import AsyncGenerator, Optional
from backend.providers.base_provider import BaseProvider
from backend.shared.logging_config import logger

class MockProvider(BaseProvider):
    """
    Mock AI Provider used when live AI provider keys are missing or API calls fail.
    Generates structured Next.js 14 application code and realistic task DAGs.
    """
    def __init__(self):
        super().__init__(api_key="mock_key", model_name="forgeai-mock-engine")

    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format_json: bool = False,
    ) -> str:
        logger.info("MockProvider executing completion fallback...")
        
        # Check prompt context for role hints
        sys_p = (system_prompt or "").upper()
        p_str = prompt.upper()

        if "PLANNER" in sys_p or "DAG" in p_str:
            return json.dumps({
                "tasks": [
                    {
                        "id": "research_design",
                        "name": "Research Design & UX Specs",
                        "agent_role": "research",
                        "dependencies": [],
                        "metadata": {"focus": "Modern Dark Glassmorphism UI"}
                    },
                    {
                        "id": "generate_code",
                        "name": "Generate Next.js 14 Web Application",
                        "agent_role": "codegen",
                        "dependencies": ["research_design"],
                        "metadata": {"stack": "Next.js App Router + Tailwind + Framer Motion"}
                    },
                    {
                        "id": "debug_build",
                        "name": "Sandbox Verification & Build Check",
                        "agent_role": "debug",
                        "dependencies": ["generate_code"],
                        "metadata": {"sandbox": "Node.js Environment"}
                    },
                    {
                        "id": "generate_docs",
                        "name": "Generate README & System Docs",
                        "agent_role": "docs",
                        "dependencies": ["debug_build"],
                        "metadata": {"output": "Markdown"}
                    }
                ]
            }, indent=2)

        elif "RESEARCH" in sys_p or "RESEARCH" in p_str:
            return json.dumps({
                "design_tokens": {
                    "primary_color": "#6366f1",
                    "accent_color": "#a855f7",
                    "background": "#0b0f19",
                    "card_bg": "rgba(15, 23, 42, 0.75)",
                    "typography": "Inter, sans-serif"
                },
                "recommended_components": [
                    "Navbar with Glassmorphism",
                    "Hero Banner with Dynamic Gradient & CTA",
                    "Interactive Feature Grid with Framer Motion",
                    "Pricing Tiers Card Grid",
                    "Responsive Footer"
                ]
            }, indent=2)

        elif "CODEGEN" in sys_p or "FILES" in p_str or "GENERATE" in sys_p:
            return json.dumps({
                "files": [
                    {
                        "path": "package.json",
                        "content": json.dumps({
                            "name": "generated-forgeai-app",
                            "version": "0.1.0",
                            "private": True,
                            "scripts": {
                                "dev": "next dev",
                                "build": "next build",
                                "start": "next start"
                            },
                            "dependencies": {
                                "next": "^14.2.0",
                                "react": "^18.3.0",
                                "react-dom": "^18.3.0",
                                "lucide-react": "^0.380.0",
                                "framer-motion": "^11.2.0",
                                "clsx": "^2.1.0",
                                "tailwind-merge": "^2.3.0"
                            },
                            "devDependencies": {
                                "typescript": "^5.4.0",
                                "@types/node": "^20.12.0",
                                "@types/react": "^18.3.0",
                                "@types/react-dom": "^18.3.0",
                                "tailwindcss": "^3.4.0",
                                "postcss": "^8.4.0",
                                "autoprefixer": "^10.4.0"
                            }
                        }, indent=2)
                    },
                    {
                        "path": "src/app/layout.tsx",
                        "content": 'import type { Metadata } from "next";\nimport "./globals.css";\n\nexport const metadata: Metadata = {\n  title: "ForgeAI Web Application",\n  description: "Generated by ForgeAI Multi-Agent System",\n};\n\nexport default function RootLayout({\n  children,\n}: {\n  children: React.ReactNode;\n}) {\n  return (\n    <html lang="en">\n      <body className="bg-[#0b0f19] text-slate-100 font-sans antialiased min-h-screen">\n        {children}\n      </body>\n    </html>\n  );\n}\n'
                    },
                    {
                        "path": "src/app/page.tsx",
                        "content": '"use client";\n\nimport React from "react";\nimport { Sparkles, ArrowRight, ShieldCheck, Zap, Layers } from "lucide-react";\n\nexport default function HomePage() {\n  return (\n    <div className="min-h-screen bg-[#0b0f19] text-white selection:bg-indigo-500 selection:text-white">\n      {/* Navigation */}\n      <nav className="fixed top-0 left-0 right-0 z-50 backdrop-blur-md bg-slate-900/60 border-b border-slate-800/80">\n        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">\n          <div className="flex items-center space-x-2">\n            <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center font-bold text-white shadow-lg shadow-indigo-500/30">\n              ⚡\n            </div>\n            <span className="font-bold text-lg tracking-wide text-white">ForgeAI App</span>\n          </div>\n          <div className="flex items-center space-x-6 text-sm">\n            <a href="#features" className="text-slate-300 hover:text-white transition">Features</a>\n            <a href="#pricing" className="text-slate-300 hover:text-white transition">Pricing</a>\n            <button className="bg-indigo-600 hover:bg-indigo-500 text-white font-medium px-4 py-2 rounded-lg shadow-md shadow-indigo-600/30 transition">\n              Get Started\n            </button>\n          </div>\n        </div>\n      </nav>\n\n      {/* Hero Section */}\n      <section className="pt-32 pb-20 px-6 max-w-5xl mx-auto text-center space-y-8">\n        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 text-sm">\n          <Sparkles className="w-4 h-4" />\n          <span>Next-Gen Web Platform</span>\n        </div>\n        <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-200 to-indigo-400 bg-clip-text text-transparent leading-tight">\n          Build Faster with Multi-Agent Intelligence\n        </h1>\n        <p className="text-lg text-slate-400 max-w-2xl mx-auto">\n          Empower your workflow with high-performance automated synthesis, modular architecture, and modern glassmorphic aesthetics.\n        </p>\n        <div className="flex items-center justify-center space-x-4">\n          <button className="bg-indigo-600 hover:bg-indigo-500 text-white font-semibold px-6 py-3 rounded-xl shadow-lg shadow-indigo-600/30 flex items-center space-x-2 transition">\n            <span>Explore Dashboard</span>\n            <ArrowRight className="w-4 h-4" />\n          </button>\n        </div>\n      </section>\n\n      {/* Feature Grid */}\n      <section id="features" className="py-20 px-6 max-w-6xl mx-auto">\n        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">\n          <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800 backdrop-blur-lg hover:border-indigo-500/40 transition">\n            <Zap className="w-8 h-8 text-indigo-400 mb-4" />\n            <h3 className="text-xl font-bold mb-2">Instant Generation</h3>\n            <p className="text-slate-400 text-sm">Turn complex prompt ideas into production-ready Next.js web applications seamlessly.</p>\n          </div>\n          <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800 backdrop-blur-lg hover:border-indigo-500/40 transition">\n            <ShieldCheck className="w-8 h-8 text-indigo-400 mb-4" />\n            <h3 className="text-xl font-bold mb-2">Automated Sandbox Check</h3>\n            <p className="text-slate-400 text-sm">Automated build verification loops ensure zero compilation errors before deployment.</p>\n          </div>\n          <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800 backdrop-blur-lg hover:border-indigo-500/40 transition">\n            <Layers className="w-8 h-8 text-indigo-400 mb-4" />\n            <h3 className="text-xl font-bold mb-2">Modular Component Architecture</h3>\n            <p className="text-slate-400 text-sm">Clean TypeScript codebase structured for scalability and easy maintenance.</p>\n          </div>\n        </div>\n      </section>\n\n      {/* Footer */}\n      <footer className="py-8 border-t border-slate-800 text-center text-slate-500 text-sm">\n        <p>© 2026 ForgeAI. All rights reserved.</p>\n      </footer>\n    </div>\n  );\n}\n'
                    },
                    {
                        "path": "src/app/globals.css",
                        "content": "@tailwind base;\n@tailwind components;\n@tailwind utilities;\n\nbody {\n  color: #f8fafc;\n  background: #0b0f19;\n}\n"
                    }
                ]
            }, indent=2)

        elif "DEBUG" in sys_p or "DEBUG" in p_str:
            return json.dumps({
                "files": []
            }, indent=2)

        elif "DOCS" in sys_p or "DOCS" in p_str:
            return json.dumps({
                "readme": "# Generated Application\n\nThis Next.js 14 web application was generated by ForgeAI Multi-Agent Builder.\n\n## Quick Start\n```bash\nnpm install\nnpm run dev\n```",
                "architecture": "Next.js 14 App Router, Tailwind CSS, Lucide React icons"
            }, indent=2)

        else:
            return json.dumps({"status": "ok", "message": "Mock provider fallback response"}, indent=2)

    async def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> AsyncGenerator[str, None]:
        res = await self.complete(prompt, system_prompt, temperature, max_tokens)
        yield res
