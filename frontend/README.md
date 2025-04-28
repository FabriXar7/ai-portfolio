# Servicio Frontend React  🎨

[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E)](https://vitejs.dev/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)


## 🚀 Instrucciones de configuración local

1. Asegurese que Node.js 20.x esta instalado

2. Instalar dependencias:
   ```bash
   npm install
   ```

3. Configurar entorno:
   ```bash
   # Crear archivo .env con:
   VITE_BACKEND_URL=http://localhost:8000  # o tu backend URL
   ```

4. Agrega tu contenido personal:
   - Add `about-me.md` to public folder
   - Add `icon.svg` to public folder
   - Add `profile.jpg` to public folder
   - Update `config.json` following the [Config Setup Guide](CONFIGURATION.md)

5. Iniciar servidor de desarrollo:
   ```bash
   npm run dev
   ```

6. Visite http://localhost:5173 para ver la aplicacion 🎉

## 🛠 Scripts de desarrollo

```bash
# Iniciar servidor de desarrollo
npm run dev

# Construir para producción
npm run build

#Vista previa de la versión de producción
npm run preview
```

## 🧪 Pruebas

Este proyecto utiliza Vitest y la biblioteca de pruebas React para realizar pruebas unitarias. Las pruebas se organizan junto con sus componentes.

### Ejecución de pruebas

```bash
# Ejecutar todas las pruebas
npm test

# Ejecutar pruebas en modo vistas
npm run test:watch

# Ejecutar pruebas con cobertura
npm test -- --coverage
```

## 🚀 Desarrollo en Vercel

1. Crear una cuenta en [Vercel.com](https://vercel.com)

2. Crea un nuevo proyecto y conéctate a tu repositorio

3. Configurar variables de entorno:
   ```bash
   VITE_BACKEND_URL=https://your-backend-url
   ```

4. ¡Implementa! Tu aplicación estará disponible en https://your-project-name.vercel.app 🎉

## 🛠 Tecnologia

- React 18
- Vite
- TailwindCSS
- Framer Motion
- React Router DOM
- ESLint

