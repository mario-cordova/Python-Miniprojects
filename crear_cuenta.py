import tkinter as tk
from tkinter import messagebox

class SistemaLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Seguridad")
        self.root.geometry("300x280")
        
        # Variables de estado (reemplazan tus returns)
        self.true_user = ""
        self.true_pass = ""
        self.intentos = 3
        
        # Iniciar directamente en la pantalla de registro
        self.pantalla_registro()

    def limpiar_pantalla(self):
        """Destruye los widgets actuales para redibujar la ventana."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def pantalla_registro(self, solo_password=False):
        self.limpiar_pantalla()
        
        tk.Label(self.root, text="--- CREAR CUENTA ---", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Si venimos de un bloqueo, solo pedimos la contraseña
        if not solo_password:
            tk.Label(self.root, text="Crea el nombre de usuario:").pack()
            self.entry_reg_user = tk.Entry(self.root)
            self.entry_reg_user.pack(pady=5)
        else:
            tk.Label(self.root, text=f"Usuario: {self.true_user}", fg="blue").pack(pady=5)
            
        tk.Label(self.root, text="Crea la contraseña:").pack()
        self.entry_reg_pass = tk.Entry(self.root, show="*") # show="*" oculta el texto
        self.entry_reg_pass.pack(pady=5)
        
        if solo_password:
            tk.Button(self.root, text="Restablecer Contraseña", command=self.guardar_solo_password).pack(pady=15)
        else:
            tk.Button(self.root, text="Registrar", command=self.guardar_registro).pack(pady=15)

    def guardar_registro(self):
        self.true_user = self.entry_reg_user.get()
        self.true_pass = self.entry_reg_pass.get()
        
        if self.true_user and self.true_pass:
            messagebox.showinfo("Éxito", "Cuenta creada exitosamente.")
            self.pantalla_login()
        else:
            messagebox.showwarning("Error", "Ambos campos son obligatorios.")

    def guardar_solo_password(self):
        self.true_pass = self.entry_reg_pass.get()
        if self.true_pass:
            messagebox.showinfo("Éxito", "Contraseña restablecida.")
            self.intentos = 3  # Reiniciamos los intentos
            self.pantalla_login()
        else:
            messagebox.showwarning("Error", "La contraseña no puede estar vacía.")

    def pantalla_login(self):
        self.limpiar_pantalla()
        
        tk.Label(self.root, text="--- INICIAR SESIÓN ---", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(self.root, text="Ingresa el usuario:").pack()
        self.entry_log_user = tk.Entry(self.root)
        self.entry_log_user.pack(pady=5)
        
        tk.Label(self.root, text="Ingresa la contraseña:").pack()
        self.entry_log_pass = tk.Entry(self.root, show="*")
        self.entry_log_pass.pack(pady=5)
        
        # Etiqueta para mostrar los mensajes de error (sustituye a los prints)
        self.lbl_mensaje = tk.Label(self.root, text="", fg="red")
        self.lbl_mensaje.pack(pady=5)
        
        tk.Button(self.root, text="Ingresar", command=self.verificar_login).pack(pady=10)

    def verificar_login(self):
        user = self.entry_log_user.get()
        password = self.entry_log_pass.get()
        
        # Lógica exacta de tu función comp()
        if password == self.true_pass and user == self.true_user:
            messagebox.showinfo("Éxito", "Bienvenido al sistema.")
            self.root.quit() # Cierra la app al tener éxito (puedes cambiarlo)
        else:
            self.intentos -= 1
            
            if user != self.true_user and password != self.true_pass:
                mensaje = "Esta ni siquiera es tu cuenta, bro."
            elif password != self.true_pass:
                mensaje = "Contraseña incorrecta. Vuelva a intentar."
            elif user != self.true_user:
                mensaje = "Nombre de usuario incorrecto. Vuelva a intentar."
                
            if self.intentos > 0:
                self.lbl_mensaje.config(text=f"{mensaje}\n(Intentos restantes: {self.intentos})")
            else:
                messagebox.showwarning("Bloqueado", "Has agotado tus 3 intentos.\nTu contraseña será restablecida.")
                self.pantalla_registro(solo_password=True)

# Bloque principal para ejecutar la app
if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = SistemaLogin(ventana_principal)
    ventana_principal.mainloop()