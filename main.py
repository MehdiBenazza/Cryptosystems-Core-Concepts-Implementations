from Symetric_Encryption.main_symetric import main as sym_main

if __name__ == "__main__":
    while True:
        print("1. Symetric Encryption")
        print("2. Asymetric Encryption")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            sym_main()
        elif choice == "2":
            print("Asymmetric Encryption menu non implémenté pour l'instant.")
        else:
            break