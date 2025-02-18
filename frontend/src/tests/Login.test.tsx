import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import Login from "../components/Login"; // Este componente aún no existe, pero lo crearemos luego

describe("Login Page", () => {
  it("debe renderizar el formulario de login", () => {
    render(<Login />);

    // Verifica que existan los campos de email y contraseña
    expect(screen.getByPlaceholderText("Email")).toBeDefined();
    expect(screen.getByPlaceholderText("Contraseña")).toBeDefined();

    // Verifica que el botón de inicio de sesión exista
    expect(screen.getByRole("button", { name: /iniciar sesión/i })).toBeDefined();
  });
});