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
                             /* |    \:.. ./                                            | */
                             /* |     `---'                                             | */
                             /* |                                                       | */
                             /* +-------------------------------------------------------+ */                                       
            -----------------------------------------------------------------------------------------------------
                                     🎉🏆BIENVENIDO A LOS SORETOS VIRTUALES 🏆🎉                                                        
                                        🚀¡Preparate para probar tu suerte!🚀                                                    
                                       Cada boleto es una oportunidad de ganar                                               
                                                  ¡COMENCEMOS! ⏳👇

                                                                                                                                                   
"""  
print (menu_inicio)
#-------------------------------------------------------------------------------------------------
def generar_numeros_ganadores():
    numeros_ganadores = [random.randint(0,9) for _ in range(6)]
    numeros_ganadores.sort()
    print ("\n 🏆LOS NUMEROS GANADORES SON: ", numeros_ganadores)
    return numeros_ganadores
#------------------------------------------------------------------------------------------------
def mostrar_reglas():

    print            ("🎲REGLAS DEL JUEGO LOTERIA🎲")
    print ("-------------------------------------------------------")
    print (  "- ¡Cada boleto debe contener exactamente 6 numeros!"  )
    print (        "- Los numeros deben estar entre 0 y 9."         )
    print (  "- No se permiten letras ni numeros fuera de ese rango.")
    print(              "\n🏆PREMIOS SEGUN ACIERTOS🏆: ")
    print(             "- 6 Aciertos 🎉 premio mayor")
    print(             "- 5 Aciertos 🎖️ premio grande")
    print(             "- 4 Aciertos 🥈 premio mediano ")
    print(             "- 3 Aciertos 🥉 premio pequeño ")
    print(            "- Menos de 3 Aciertos😢 Sin premio")
    print ("-------------------------------------------------------")
#--------------------------------------------------------------------------------------------------
def comprar_boletos(): 
    mostrar_reglas()
    try:
        usuarios = int(input("👤 ¿Cuántas personas van a comprar boletos?: "))
    except ValueError:
        print("🚨 Debes escribir un número entero. Cerrando programa. 🚨")
        return

    boletos = []  # Lista para guardar datos para JSON

    with open('boletos_loteria.csv', mode='a', newline="") as archivo_csv:
        escritor = csv.writer(archivo_csv)

        for i in range(usuarios):
            print(f"\n Usuario {i + 1} ")
            nombre = input("Por favor, ingresa tu nombre: ")

            print(f"\n ¡Hola {nombre}! 🎉 Bienvenido a la lotería 🎉")
            print("Aquí podrás comprar boletos.\n")

            try: 
                cantidad_boletos = int(input(f"💸 ¿Cuántos boletos deseas comprar, {nombre}?: "))
            except ValueError: 
                print("🚨 Entrada inválida. Se asignará 1 boleto por defecto. 🚨")
                cantidad_boletos = 1

            for b in range(cantidad_boletos):
                print(f"\n Boleto {b + 1} de {cantidad_boletos}")
                numeros = []

                while len(numeros) < 6:  # Cambié a 6 números por boleto
                    try:
                        numero = int(input(f"🎫 Ingrese un número de 0 a 9: -{len(numeros) + 1}: "))
                        if numero < 0 or numero > 9: 
                            print("❗El número debe estar dentro del rango permitido❗")
                            continue 
                        numeros.append(numero)

                    except ValueError:
                        print("🚨 Debes escribir un número válido. 🚨")

                boleto_final = numeros.copy()
                print("\n Tu boleto es:", boleto_final)
                escritor.writerow([nombre, f"boleto {b + 1}"] + boleto_final)
                
                boletos.append({
                    "nombre": nombre,
                    "boleto": f"boleto {b + 1}",
                    "numeros": boleto_final
                })
                print("✔️ Tu boleto ha sido guardado exitosamente! ✔️")

    with open("historial.json", "w") as json_file:
        json.dump(boletos, json_file, indent=4)
#---------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

def comparar_boletos (numeros_ganadores):
    print ("\n 📋RESULTADOS DE LA LOTERIA📋:" )
    print (f" 🎉NUMEROS GANADORES🎉: {numeros_ganadores}\n")

    try: 
    
        with open ('boletos_loteria.csv', mode='r') as archivo:
            lector = csv.reader (archivo)
            for fila in lector:
                if fila:
                    nombre = fila [0]
                    numero_boleto = fila[1]
                    numeros_usuarios = list(map(int,fila[2:]))

                    #COMPARAR POSICION POR POSICION 
                    coincidencias = sum(1 for a,b in zip(numeros_usuarios,numeros_ganadores) if a==b)
                    posiociones_acertadas= [i+1 for i,(a, b)in enumerate(zip(numeros_usuarios, numeros_ganadores))if a ==b]

                   #determinar premios por coincidencias exactas 
                    if coincidencias == 6:
                        premio = "🏆 Premio Mayor "
                    elif coincidencias == 5:
                        premio = "🥇  Premio Grande "
                    elif coincidencias == 4:
                        premio = "🥈 Premio Mediano "
                    elif  coincidencias == 3:
                        premio = "🥉 Premio Pequeño"
                    else: 
                        premio = "Sin premio"

                    print (f"{nombre} - {numero_boleto} tuvo {coincidencias} aciertos en posicion {posiociones_acertadas} con el boleto {numeros_usuarios} -> {premio} ")

    except FileNotFoundError:
        print ("Aun no hay datos para comparar.")

#----------------------------------------------------------------------------------------------------------------------------

def ver_historial():
    print ("\n HISTORIAL DE BOLETOS: ")
    try: 
        with open ('boletos_loteria.csv',mode='r') as archivo:
            lector = csv.reader(archivo)
            for fila in lector:
                if fila:
                    nombre = fila[0]
                    numero_boleto = fila [1]
                    numeros = fila [2:]
                    print (f"{nombre} - {numero_boleto}: {numeros}")
    except FileNotFoundError:
        print ("No se encontro ningin historial.Juega primero")

#------------------------------------------------------------------------------------------------------------------------------
def juego_adivina ():
    print ("\n🎮  BIENVENIDO AL JUEGO 'ADIVINA EL NUMERO SECRETO'🎮 ")
    print ("                   🧾REGLAS DEL JUEGO:                   ")
    print ("1. 👤Debes ser mayor de 18 años para participar.    ")
    print ("2. El sistema escogera un numero entre 1 y 35.")
    print ("3. Tienes 5 intentos para adivinar el numero.")
    print ("4. 💸 Si aciertas,¡Ganas 1.000.000 de dolares!💸" )

    #solicitamos la edad y el nombre

    nombre = input ("\n👥 Ingresa tu nombre: ")
    try:
        edad = int(input(" Ingresa tu edad:"))
    except ValueError:
        print ("🚨 Edad invalida. Saliendo del juego. ")
        return
    
    if edad < 18:
        print ("🚨 Lo sentimos, debes ser mayor de edad para jugar. ")
        return
    
    numero_secreto = random.randint(1,35)
    intentos = 5 
    
    for intento in range(1, intentos + 1 ):
        try:
            eleccion = int(input(f" Intento {intento}/{intentos} - Adivina el numero (1 al 35): "))
            if eleccion < 1 or eleccion > 35 :
                print ("Numeeo fuera de rango. Intenta Nuevamente. ")
                continue
            if eleccion == numero_secreto:
                print (" ¡CORRECTO!")
                print("🏆 ¡Has ganado el gran premio de $1.000.000de dolares! 💰")
                guardar_historial_juego(nombre, edad, "Gano", "$1.000.000")
                return 
            elif eleccion < numero_secreto:
                   print("📉 Muy bajo. Intenta un numero mas alto.")
            else:
                print("📈 Muy alto. Intenta un numero mas bajo.")
        except ValueError:
            print("🚨 Ingresa un numero valido.")

    print (f"m Lo siento, {nombre}. El numero secreto era {numero_secreto}.")
    print (" Concejo: ¡Vuelve a intertarlo, La proxima puedes ganar! ")
    guardar_historial_juego(nombre, edad, "Perdio")


#---------------------------------------------------------------------------------------------------------------------------------
def guardar_historial_juego (nombre, edad, resultado, premio=""):
    with open ('historial_juego_adivina.csv', mode='a', newline='') as archivo:
        escritor = csv.writer (archivo)
        escritor.writerow([nombre, edad, resultado, premio])


#-----------------------------------------------------------------------------------------------------------------------------------
def ver_historial_adivina ():
    print ("\n HISTORIAL DEL JUEGO 'ADIVINA EL NUMERO SECRETO':")
    try:
        with open ('historial_juego_adivina.csv', mode='r' ) as archivo :
            lector = csv.reader(archivo)
            for fila in lector :
                if fila:
                    nombre, edad, resultado, premio = fila
                    print (f"{nombre} ({edad} años) - Resultado: {resultado} {'💰 Premio: ' + premio if premio else ''}")

    except FileNotFoundError:
        print (" No hay historial aun. Juega primero.")
#-----------------------------------------------------------------------------------------------------------------------------------



while True:
    print ("\n MENU PRINCIPAL ") 
    print ("1. 🎟️ Comprar boleta ")
    print ("2. 📄 Ver historial de la loteria  ")
    print ("3. 🎰 Ejecutar sorteo y comparar resultados")
    print ("4. 🎮 Jugar 'Adivina el número secreto")
    print ("5. 📘 Ver historial del juego 'Adivina el número secreto'")
    print ("6. ❌ SALIR  ")

    opcion = input("Seleciona una opcion: ")
    
    if opcion =="1":
        comprar_boletos()
    elif opcion =='2':
        ver_historial()
    elif opcion =='3':
        numeros_ganadores = generar_numeros_ganadores()
        comparar_boletos(numeros_ganadores)
    elif opcion == '4': 
        juego_adivina()
    elif opcion == '5':
        ver_historial_adivina()
    elif opcion == '6':
        print ("¡Gracias por participar!¡BUENA SUERTE!")
        break
    else:
        print (" Opcion invalida intente de nuevo")


#tratar de comparar los numeros que estan bien 
