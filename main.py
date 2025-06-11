import json 
import csv 
import random
import os 

menu_inicio = """
                             /* +-------------------------------------------------------+ */
                             /* |                                                       | */
                             /* |    _______            __                              | */
                             /* |   |   _   .-----.----|  |_.-----.-----.-----.         | */
                             /* |   |   1___|  _  |   _|   _|  -__|  _  |__ --|         | */
                             /* |   |____   |_____|__| |____|_____|_____|_____|         | */
                             /* |   |:  1   |                                           | */
                             /* |   |::.. . |                                           | */
                             /* |   `-------'                                           | */
                             /* |    ___ ___ __      __               __                | */
                             /* |   |   Y   |__.----|  |_.--.--.---.-|  .-----.-----.   | */
                             /* |   |.  |   |  |   _|   _|  |  |  _  |  |  -__|__ --|   | */
                             /* |   |.  |   |__|__| |____|_____|___._|__|_____|_____|   | */
                             /* |   |:  1   |                                           | */
                             /* |   ||     ||                                           | */
                             /* |     `---'                                             | */
                             /* |                                                       | */
                             /* +-------------------------------------------------------+ */                                       
            -----------------------------------------------------------------------------------------------------
                                        🎉🏆BIENVENIDO A MI LOTERIA VIRTUAL🏆🎉                                                        
                                          🚀¡Preparate para probar tu suerte!🚀                                                    
                                      🎫¡Cada boleto es una oportunidad de ganar!🎫                                               
                                                   💸¡COMENCEMOS! ⏳👇
"""  
print(menu_inicio)

#-------------------------------------------------------------------------------------------------------------------
def mostrar_reglas():
    print("\n🎲REGLAS DEL JUEGO LOTERIA🎲")
    print("-" * 50)
    print("- ¡Cada boleto debe contener exactamente 6 numeros!")
    print("- No se permiten letras ni numeros fuera de ese rango.")
    print("- Los numeros deben estar entre 0 y 9.")
    print("\n🏆PREMIOS SEGUN ACIERTOS🏆:")
    print("- 6 Aciertos 🎉 premio mayor")
    print("- 5 Aciertos 🎖️ premio grande")
    print("- 4 Aciertos 🧈 premio mediano")
    print("- 3 Aciertos 🥉 premio pequeño")
    print("- Menos de 3 Aciertos😢 Sin premio")
    print("-" * 50)

#-------------------------------------------------------------------------------------------------------------------
def comprar_boletos():
    mostrar_reglas()
    try:
        usuarios = int(input("\n👤 ¿Cuantas personas van a comprar boletos?: "))
    except ValueError:
        print("🚨 Debes escribir un numero entero. Cerrando programa. 🚨")
        return

    boletos = []

    with open('boletos_loteria.csv', mode='a', newline="") as archivo_csv:
        escritor = csv.writer(archivo_csv)

        for i in range(usuarios):
            print(f"\n Usuario {i + 1} ")
            nombre = input("Por favor, ingresa tu nombre: ")

            print(f"\n ¡Hola {nombre}! 🎉 Bienvenido a la loteria 🎉")
            print("Aqui podras comprar boletos.\n")

            try:
                cantidad_boletos = int(input(f"💸 ¿Cuantos boletos deseas comprar, {nombre}?: "))
            except ValueError:
                print("🚨 Entrada invalida. Se asignara 1 boleto por defecto. 🚨")
                cantidad_boletos = 1

            for b in range(cantidad_boletos):
                print(f"\n Boleto {b + 1} de {cantidad_boletos}")
                numeros = []
                while len(numeros) < 6:
                    try:
                        numero = int(input(f"🎫 Ingrese un numero de 0 a 9: "))
                        if numero < 0 or numero > 9:
                            print("❗El numero debe estar dentro del rango permitido❗")
                            continue
                        numeros.append(numero)
                    except ValueError:
                        print("🚨 Debes escribir un numero valido. 🚨")

                boleto_final = numeros.copy()
                print("\n Tu boleto es:", boleto_final)
                escritor.writerow([nombre, f"boleto {b + 1}"] + boleto_final)

                boletos.append({"nombre": nombre, "boleto": f"boleto {b + 1}", "numeros": boleto_final})
                print("✔️ Tu boleto ha sido guardado exitosamente! ✔️")

    with open("historial.json", "w") as json_file:
        json.dump(boletos, json_file, indent=4)

#-------------------------------------------------------------------------------------------------------------------
def generar_numeros_ganadores():
    numeros_ganadores = [random.randint(0, 9) for _ in range(6)]
    numeros_ganadores.sort()
    print("\n 🏆LOS NUMEROS GANADORES SON:", numeros_ganadores)
    return numeros_ganadores

#-------------------------------------------------------------------------------------------------------------------
def comparar_boletos(numeros_ganadores):
    print("\n 📋RESULTADOS DE LA LOTERIA📋:")
    print(f" 🎉NUMEROS GANADORES🎉: {numeros_ganadores}\n")

    try:
        with open('boletos_loteria.csv', mode='r') as archivo:
            lector = csv.reader(archivo)
            print("-" * 110)
            print(f"{'Nombre':<15} {'Boleto':<10} {'Aciertos':<10} {'Posiciones':<25} {'Numeros':<30} {'Premio'}")
            print("-" * 110)

            for fila in lector:
                if fila:
                    nombre = fila[0]
                    numero_boleto = fila[1]
                    numeros_usuarios = list(map(int, fila[2:]))

                    coincidencias = sum(1 for a, b in zip(numeros_usuarios, numeros_ganadores) if a == b)
                    posiciones_acertadas = [i + 1 for i, (a, b) in enumerate(zip(numeros_usuarios, numeros_ganadores)) if a == b]

                    if coincidencias == 6:
                        premio = "🏆 Premio Mayor - 💰🎉¡GANASTE 50 MIL MILLONES DE DOLARES!🎉💰"
                    elif coincidencias == 5:
                        premio = "🥇 Premio Grande -💸¡GANASTE $4.000.000 DOLARES!💸"
                    elif coincidencias == 4:
                        premio = "🥈 Premio Mediano -💸¡GANASTE 500.000 DOLARES!💸"
                    elif coincidencias == 3:
                        premio = "🥉 Premio Pequeño -💸¡GANASTE 50.000 DOLARES!💸"
                    else:
                        premio = "Sin premio - Compra otro boleto"

                    print(f"{nombre:<15} {numero_boleto:<10} {coincidencias:<10} {str(posiciones_acertadas):<25} {str(numeros_usuarios):<30} {premio}")
                    print("-" * 110)
    except FileNotFoundError:
        print("Aun no hay datos para comparar.")

#-------------------------------------------------------------------------------------------------------------------
def ver_historial():
    print("\n📘 HISTORIAL DE BOLETOS: ")
    try:
        with open('historial.json', 'r') as archivo_json:
            historial = json.load(archivo_json)
            print(f"{'Nombre':<15} {'Boleto':<10} {'Números'}")
            print("-" * 50)
            for entrada in historial:
                nombre = entrada.get("nombre", "Desconocido")
                boleto = entrada.get("boleto", "Sin nombre")
                numeros = entrada.get("numeros", [])
                print(f"{nombre:<15} - {boleto:<10}: {', '.join(map(str, numeros))}")
    except FileNotFoundError:
        print("No se encontro ningún historial. Juega primero.")
    except json.JSONDecodeError:
        print("Error al leer el archivo JSON. Esta vacio")

#-------------------------------------------------------------------------------------------------------------------
def juego_adivina():
    print("\n🎮 BIENVENIDO AL JUEGO 'ADIVINA EL NUMERO SECRETO' 🎮")
    print("                 REGLAS DEL JUEGO:                      ")
    print("     1. 👤 Debes ser mayor de 18 años para participar.")
    print("     2. El sistema escogera un número entre 1 y 35.")
    print("     3. Tienes 5 intentos para adivinar el numero.")
    print("     4. 💸 Si aciertas, ¡ganas 1.000.000 de dolares!")

    nombre = input("\n👥 Ingresa tu nombre: ")
    try:
        edad = int(input("Ingresa tu edad: "))
    except ValueError:
        print("🚨 Edad invalida. Saliendo del juego.")
        return

    if edad < 18:
        print("🚨 Lo sentimos, debes ser mayor de edad para jugar.")
        return

    numero_secreto = random.randint(1, 35)
    intentos = 5

    for intento in range(1, intentos + 1):
        try:
            eleccion = int(input(f"Intento {intento}/{intentos} - Adivina el número (1 al 35): "))
            if eleccion < 1 or eleccion > 35:
                print("Numero fuera de rango. Intenta nuevamente.")
                continue
            if eleccion == numero_secreto:
                print("\n🎉 ¡CORRECTO!")
                print("🏆 ¡Has ganado el gran premio de $1.000.000 de dólares! 💰")
                guardar_historial_juego(nombre, edad, "Gano", "$1.000.000 Dolares")
                return
            elif eleccion < numero_secreto:
                print("📉 Muy bajo. Intenta un numero más alto.")
            else:
                print("📈 Muy alto. Intenta un numero más bajo.")
        except ValueError:
            print("🚨 Ingresa un numero valido.")

    print(f"\nLo siento, {nombre}. El número secreto era {numero_secreto}.")
    print("Consejo: ¡Vuelve a intentarlo, la proxima puedes ganar!")
    guardar_historial_juego(nombre, edad, "Perdio")

#-------------------------------------------------------------------------------------------------------------------
def guardar_historial_juego(nombre, edad, resultado, premio=""):
    entrada = {
        "nombre": nombre,
        "edad": edad,
        "resultado": resultado,
        "premio": premio
    }
    historial = []
    if os.path.exists('historial_juego_adivina.json') and os.path.getsize('historial_juego_adivina.json') > 0:
        with open('historial_juego_adivina.json', 'r') as archivo:
            historial = json.load(archivo)
    historial.append(entrada)
    with open('historial_juego_adivina.json', 'w') as archivo:
        json.dump(historial, archivo, indent=4)

#-------------------------------------------------------------------------------------------------------------------
def ver_historial_adivina():
    print("\n📘 HISTORIAL DEL JUEGO 'ADIVINA EL NUMERO SECRETO':")
    if not os.path.exists('historial_juego_adivina.json') or os.path.getsize('historial_juego_adivina.json') == 0:
        print("❌ No hay historial aun. Juega primero.")
        return
    try:
        with open('historial_juego_adivina.json', 'r') as archivo:
            historial = json.load(archivo)
        print(f"{'Nombre':<12} {'Edad':<5} {'Resultado':<10} {'Premio':<20}")
        print("-" * 55)
        for entrada in historial:
            print(f"{entrada['nombre']:<12} {entrada['edad']:<5} {entrada['resultado']:<10} {entrada['premio']:<20}")
    except json.JSONDecodeError:
        print("❌ Error al leer el archivo JSON.")

#-------------------------------------------------------------------------------------------------------------------

while True:
    print("\n MENU PRINCIPAL")
    print("1. 🎟️ Comprar boleta")
    print("2. 📄 Ver historial de la loteria")
    print("3. 🌀 Ejecutar sorteo y comparar resultados")
    print("4. 🎮 Jugar 'Adivina el numero secreto'")
    print("5. 📘 Ver historial del juego 'Adivina el numero secreto'")
    print("6. ❌ SALIR")

    opcion = input("Selecciona una opcion: ")
    if opcion == "1":
        comprar_boletos()
    elif opcion == "2":
        ver_historial()
    elif opcion == "3":
        numeros_ganadores = generar_numeros_ganadores()
        comparar_boletos(numeros_ganadores)
    elif opcion == "4":
        juego_adivina()
    elif opcion == "5":
        ver_historial_adivina()
    elif opcion == "6":
        print("¡Gracias por participar! ¡BUENA SUERTE!")
        break
    else:
        print("Opcion invalida, intenta de nuevo.")




