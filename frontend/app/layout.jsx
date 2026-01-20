import '@/styles/globals.css';
import { LanguageProvider } from '@/lib/languageContext';

export const metadata = {
  title: 'VozPública',
  description: 'Análisis de discurso político con IA',
  icons: {
    icon: '/favicon.svg',
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="es">
      <body>
        <LanguageProvider>
          {children}
        </LanguageProvider>
      </body>
    </html>
  );
}
