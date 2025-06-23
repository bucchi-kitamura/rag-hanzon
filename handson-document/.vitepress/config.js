import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "RAG Hanzon",
  description: "A hands-on guide to building a local RAG system",
  base: '/rag-hanzon/',
  
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
    ],

    sidebar: [
      {
        text: 'Getting Started',
        items: [
          { text: 'はじめに', link: '/' },
          { text: '事前準備', link: '/guide/preparation' },
          { text: '環境構築', link: '/guide/setup' },
          { text: 'Step1 チャット機能', link: '/handson/chat' },
          { text: 'Step2 RAG機能', link: '/handson/rag' },
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/kitamuratakashi/rag-hanzon' }
    ]
  }
})