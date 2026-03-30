import Symetric_Encryption
import Asymetric_Encryption

if __name__ == "__main__":
    while True:
        print("1. Symetric Encryption")
        print("2. Asymetric Encryption")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            Symetric_Encryption.main()
        elif choice == "2":
            Asymetric_Encryption.main()
        else:
            break