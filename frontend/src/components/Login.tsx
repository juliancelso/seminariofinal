import { useState } from "react";

const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault(); // Evitar que el formulario se recargue

        setError(""); // Limpiar errores antes de una nueva petición

        try {
            const response = await fetch("http://127.0.0.1:8000/api/auth/login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem("token", data.token); // Guardar token en localStorage
                alert("Login exitoso 🎉");
                window.location.href = "/dashboard"; // 🔹 Redirigir al dashboard
            } else {
                setError(data.error || "Error en el login");
            }
        } catch (err) {
            setError("Error de conexión con el servidor");
        }
    };

    return (
        <section className="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-gray-900">
            <div className="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-lg w-96 h-auto py-12">
                <h1 className="text-2xl font-semibold text-gray-900 dark:text-white text-center mb-6">
                    Iniciar sesión
                </h1>
                <form className="space-y-4" onSubmit={handleLogin}>
                    <div>
                        <label
                            htmlFor="email"
                            className="block text-sm font-medium text-gray-700 dark:text-gray-300"
                        >
                            Correo electrónico
                        </label>
                        <input
                            type="email"
                            id="email"
                            placeholder="tu@email.com"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="mt-1 w-full p-2.5 border border-gray-300 rounded-lg shadow-sm focus:ring-black focus:border-black dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"
                            required
                        />
                    </div>
                    <div>
                        <label
                            htmlFor="password"
                            className="block text-sm font-medium text-gray-700 dark:text-gray-300"
                        >
                            Contraseña
                        </label>
                        <input
                            type="password"
                            id="password"
                            placeholder="••••••••"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="mt-1 w-full p-2.5 border border-gray-300 rounded-lg shadow-sm focus:ring-black focus:border-black dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"
                            required
                        />
                    </div>
                    <button
                        type="submit"
                        className="w-full border border-black text-black dark:text-white dark:border-white rounded-lg py-2.5 font-semibold hover:bg-gray-200 dark:hover:bg-gray-700 transition-all"
                    >
                        Iniciar sesión
                    </button>
                    {error && <p className="text-red-500 text-sm text-center mt-2">{error}</p>}
                    <p className="text-sm text-center text-gray-500 dark:text-gray-400 mt-4">
                        ¿Tienes problemas para acceder?
                        <br />
                        <a href="#" className="font-medium text-black hover:underline dark:text-white">
                            Recuperar cuenta
                        </a>
                    </p>
                </form>
            </div>
        </section>
    );
};

export default Login;