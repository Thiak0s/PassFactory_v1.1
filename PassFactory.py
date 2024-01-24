import argparse
import os
import pyperclip
import random
import string
from termcolor import colored

def print_author_info():
    print(colored("  _____              ______         _                   ", color="cyan", attrs=["bold"]))
    print(colored(" |  __ \\            |  ____|       | |                  ", color="cyan", attrs=["bold"]))
    print(colored(" | |__) |_ _ ___ ___| |__ __ _  ___| |_ ___  _ __ _   _ ", color="cyan", attrs=["bold"]))
    print(colored(" |  ___/ _` / __/ __|  __/ _` |/ __| __/ _ \\| '__| | | |", color="cyan", attrs=["bold"]))
    print(colored(" | |  | (_| \\__ \\__ \\ | | (_| | (__| || (_) | |  | |_| |", color="cyan", attrs=["bold"]))
    print(colored(" |_|   \\__,_|___/___/_|  \\__,_|\\___|\\__\\___/|_|   \\__, |", color="cyan", attrs=["bold"]))
    print(colored("                                                  __/ |", color="cyan", attrs=["bold"]))
    print(colored("                                                 |___/ ", color="cyan", attrs=["bold"]))
    print(colored("\n\t\t\t\t\t\t\tv1.1.2\n", color="red", attrs=["bold"]))
    print("\n--- Información del Autor y Descripción ---\n")
    print(colored("******** ¡Esto es ", color="white") + colored("PassFactory v1.1", color="cyan", attrs=["bold"]) + colored("! *******\n", color="white"))
    print("[Herramienta creada por " + colored("thiak0s", color="yellow") + " - 2024]\n")
    print("Utilidad para generar contraseñas y diccionarios personalizados, diseñada para usuarios avanzados en ciberseguridad y pentesting.\n")
    print(colored("***** Recuerda utilizar esta herramienta de manera ética y responsable. *****\n", color="white"))

def generate_passwords(args):
    char_sets = {
        "d": string.digits,
        "L": string.ascii_lowercase,
        "c": string.ascii_uppercase,
        "s": string.punctuation,
        "include_chars": args.include_chars
    }

    selected_sets = [char_sets[set_type] for set_type in args.base if set_type in char_sets]
    all_chars = "".join(selected_sets)

    exclude_chars_set = set(args.exclude_chars)
    all_chars = "".join(char for char in all_chars if char not in exclude_chars_set)

    if args.exclude_similar:
        all_chars = "".join(char for char in all_chars if char not in "o0il1")

    if args.exclude_ambiguous:
        all_chars = "".join(char for char in all_chars if char not in "~;:.{}<>[]()/`")

    password_list = []

    for _ in range(args.num_pass):
        password = ""

        if args.begins_with == "l":
            password += random.choice(string.ascii_letters)
        elif args.begins_with == "n":
            password += random.choice(string.digits)

        remaining_length = args.length - len(password)

        if remaining_length > 0:
            password += "".join(random.choice(all_chars) for _ in range(remaining_length))

        if args.ends_with == "l":
            password += random.choice(string.ascii_letters)
        elif args.ends_with == "n":
            password += random.choice(string.digits)

        if args.no_duplicate:
            password = "".join(sorted(set(password), key=password.index))
        
        if args.output:
            save_path = args.output
        else:
            save_path = os.path.join(os.getcwd(), "passwords.txt")

        with open(save_path, 'w') as f:
            f.write("\n".join(password_list))
        
        password += random.choice(string.ascii_letters) * max(0, args.length - len(password))
        password_list.append(password[:args.length])

    return password_list

def copy_to_clipboard(passwords, copy_all=True):
    password_str = "\n".join(passwords)
    pyperclip.copy(password_str)
    print("¡Se han copiado todas las contraseñas al portapapeles!" if copy_all else "¡Se ha copiado la primera contraseña al portapapeles!")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Generador de Contraseñas - PassFactory v1.0")

    parser.add_argument("-base", dest="base", choices=["d", "L", "c", "dL", "dc", "Lc", "dLc", "dLcs"], required=True,
                        help="Elija de (d, L, c, dL, dc, Lc, dLc, dLcs).\n"
                             "d: Dígitos [0-9]\n"
                             "L: Letras minúsculas [a-z]\n"
                             "c: Letras mayúsculas [A-Z]\n"
                             "dL: Dígitos y letras minúsculas\n"
                             "dc: Dígitos y letras mayúsculas\n"
                             "Lc: Letras minúsculas y mayúsculas\n"
                             "dLc: Dígitos, letras minúsculas y mayúsculas\n"
                             "dLcs: Dígitos, letras minúsculas, mayúsculas y caracteres especiales\n")

    parser.add_argument("--len", dest="length", type=int, required=True, help="Longitud de la contraseña")

    parser.add_argument("--include_chars", dest="include_chars", default="", help="Caracteres adicionales a incluir")

    parser.add_argument("--exclude_chars", dest="exclude_chars", default="", help="Caracteres a excluir")

    parser.add_argument("--begins_with", dest="begins_with", choices=["l", "n"], help="Comenzar con cualquier letra o número")

    parser.add_argument("--ends_with", dest="ends_with", choices=["l", "n"], help="Terminar con cualquier letra o número")

    parser.add_argument("--exclude_similar", dest="exclude_similar", action="store_true", help="Excluir caracteres similares")

    parser.add_argument("--exclude_ambiguous", dest="exclude_ambiguous", action="store_true", help="Excluir caracteres ambiguos")

    parser.add_argument("--no_duplicate", dest="no_duplicate", action="store_true", help="No permitir caracteres duplicados")

    parser.add_argument("--num_pass", dest="num_pass", type=int, default=1, help="Número de contraseñas a generar")

    parser.add_argument("-o", "--output", dest="output", default="", help="Ruta de salida para el archivo de contraseñas. Si no se proporciona, se guardará en el directorio actual con el nombre 'passwords.txt'.")
    parser.add_argument("-np", "--no_print", dest="no_print", action="store_true", help="No imprimir las contraseñas en pantalla")
    parser.add_argument("-x", "--exit_after_generation", dest="exit_after_generation", action="store_true", help="Salir directamente después de generar las contraseñas")

    return parser.parse_args()

def main():

    print_author_info()

    args = parse_arguments()

    passwords = generate_passwords(args)
    
    if not args.no_print:
        print("\nContraseñas Generadas:\n")
        for password in passwords:
            print(password)
        print("\n")

    if not args.exit_after_generation:
        while True:
            print("\nOpciones:")
            print("1. Copiar todas las contraseñas al portapapeles")
            print("2. Copiar la primera contraseña al portapapeles")
            print("3. Salir (q)")

            choice = input("Ingrese el número de la opción deseada: ")

            if choice == "1":
                copy_to_clipboard(passwords)
                break
            elif choice == "2":
                copy_to_clipboard(passwords, copy_all=False)
                break
            elif choice.lower() in ["3", "q"]:
                break
            else:
                print("Opción no válida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()