import '@/styles/globals.css';

export const metadata = {
  title: 'VozPública',
  description: 'Análisis de discurso político con IA',
};

export default function RootLayout({ children }) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
