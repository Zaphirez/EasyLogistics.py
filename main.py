import pandas as pd


def remove_zero_amount_rows(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Remove rows where the "Amount" column is zero
    df = df[df["Amount"] != 0]

    # Save the updated data back to the same CSV file
    df.to_csv(csv_file, index=False)


def isvalid(a):
    vs = pd.read_csv("data/valid_storage.csv")
    if a in vs["Storage"].values:
        print(f"Found {a}!")
        return True
    else:
        print(f"No Storage named {a} Found!")
        return False


def readEAN(a):
    a = int(a)
    sd = pd.read_csv("data/stored_data.csv")
    if a in sd["EAN"].astype(int).values:
        print(f"EAN {a} Found!")
        print(sd.values)
        return True
    else:
        print(f"{a} not Found!")
        return False


def readStorage(a):
    a = str(a)
    sd = pd.read_csv("data/stored_data.csv")
    if isvalid(a):
        if sd[sd["Storage"] == a].empty:
            print("Error 404!")
            return False
        else:
            print(sd[sd["Storage"] == a].values)
            print("Done!")
            return True
    else:
        print("Invalid Storage!")


def addStorage(a):
    a = str(a)
    vs = pd.read_csv("data/valid_storage.csv")
    if vs[vs["Storage"] == a].empty:
        new_row = {"Storage": a}
        new_vs = pd.DataFrame([new_row])
        vs = pd.concat([vs, new_vs], ignore_index=True)
        vs.to_csv("data/valid_storage.csv", index=False)
        print(f"Storage {a} Added!")
    else:
        print(f"Storage {a} already Exists!")


def STOREEAN(Storage, EAN, Amount):
    Amount = int(Amount)
    EAN = int(EAN)
    sd = pd.read_csv("data/stored_data.csv")
    if isvalid(Storage):
        new_row = {"Storage": Storage, "EAN": str(EAN), "Amount": Amount}
        new_sd = pd.DataFrame([new_row])
        sd = pd.concat([sd, new_sd], ignore_index=True)
        sd.to_csv("data/stored_data.csv", index=False)
        print(f"Added {Amount}x {EAN} to {Storage}!")
        return True
    else:
        print("Not a Valid Storage!")
        return False


def relocateEAN(Storagefrom, EAN, Amount, Storageto):
    Storagefrom = str(Storagefrom)
    Storageto = str(Storageto)
    EAN = int(EAN)
    Amount = int(Amount)
    sd = pd.read_csv("data/stored_data.csv")
    if isvalid(Storagefrom) and isvalid(Storageto):
        mask = (sd["Storage"] == Storagefrom) & (sd["EAN"] == EAN) & (sd["Amount"] >= Amount)
        if not sd.loc[mask].empty:
            print("Found Storage ready for Relocation!")
            sd.loc[mask, "Amount"] -= Amount
            new_row = {"Storage": Storageto, "EAN": EAN, "Amount": Amount}
            new_sd = pd.DataFrame([new_row])
            sd = pd.concat([sd, new_sd], ignore_index=True)
            sd.to_csv("data/stored_data.csv", index=False)
            return True
        else:
            print("Something went wrong not ready for Relocation!")
            return False
    elif not isvalid(Storageto):
        print(f"Couldn't find {Storageto}")
    elif not isvalid(Storagefrom):
        print(f"Couldn't find {Storagefrom}")


relocateEAN("FB-2", 10001, 2, "FB-1")
remove_zero_amount_rows("data/stored_data.csv")
