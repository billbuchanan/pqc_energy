# This program runs a certain algorithm for a certain number of keys
# It then takes the length of time for the creation of all the keys
# and takes a measure of baseline and on-load Wattage (as user inputs)
# It then measures the power consumption of the algorithm by multiplying the time taken by the difference in wattage (on-load - baseline)
# Finally, it saves the results to a timestamped text file named after the machine.
# OG 22/03

import time
import subprocess
import platform
import datetime

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = platform.node() + "_" + timestamp + ".txt"

results = []
results.append("Machine: " + platform.node())
results.append("Platform: " + platform.machine())
results.append("System: " + platform.system())
results.append("Date: " + timestamp)
results.append("")
# ── Key Generation Functions ──────────────────────────────────────────────────

# Classical
def generate_RSA_keys():
    """Generate RSA-2048 key pair"""
    subprocess.run(["openssl", "genrsa", "-out", "private.key", "2048"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["openssl", "rsa", "-in", "private.key", "-pubout", "-out", "public.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def generate_ECDH_keys():
    """Generate ECDH P-256 key pair"""
    subprocess.run(["openssl", "genpkey", "-algorithm", "EC", "-pkeyopt", "ec_paramgen_curve:P-256", "-out", "private.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["openssl", "pkey", "-in", "private.key", "-pubout", "-out", "public.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def generate_X25519_keys():
    """Generate X25519 key pair"""
    subprocess.run(["openssl", "genpkey", "-algorithm", "X25519", "-out", "private.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["openssl", "pkey", "-in", "private.key", "-pubout", "-out", "public.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def generate_ECDSA_keys():
    """Generate ECDSA P-256 key pair"""
    subprocess.run(["openssl", "genpkey", "-algorithm", "EC", "-pkeyopt", "ec_paramgen_curve:P-256", "-out", "private.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["openssl", "pkey", "-in", "private.key", "-pubout", "-out", "public.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ML-KEM (FIPS 203) - Key Encapsulation
def generate_ML_KEM_512_keys():
    """Generate ML-KEM-512 key pair"""
    subprocess.run(["openssl", "genpkey", "-algorithm", "ML-KEM-512", "-out", "private.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["openssl", "pkey", "-in", "private.key", "-pubout", "-out", "public.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def generate_ML_KEM_768_keys():
    """Generate ML-KEM-768 key pair"""
    subprocess.run(["openssl", "genpkey", "-algorithm", "ML-KEM-768", "-out", "private.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["openssl", "pkey", "-in", "private.key", "-pubout", "-out", "public.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def generate_ML_KEM_1024_keys():
    """Generate ML-KEM-1024 key pair"""
    subprocess.run(["openssl", "genpkey", "-algorithm", "ML-KEM-1024", "-out", "private.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["openssl", "pkey", "-in", "private.key", "-pubout", "-out", "public.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ML-DSA (FIPS 204) - Digital Signatures
def generate_ML_DSA_44_keys():
    """Generate ML-DSA-44 key pair"""
    subprocess.run(["openssl", "genpkey", "-algorithm", "ML-DSA-44", "-out", "private.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["openssl", "pkey", "-in", "private.key", "-pubout", "-out", "public.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def generate_ML_DSA_65_keys():
    """Generate ML-DSA-65 key pair"""
    subprocess.run(["openssl", "genpkey", "-algorithm", "ML-DSA-65", "-out", "private.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["openssl", "pkey", "-in", "private.key", "-pubout", "-out", "public.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def generate_ML_DSA_87_keys():
    """Generate ML-DSA-87 key pair"""
    subprocess.run(["openssl", "genpkey", "-algorithm", "ML-DSA-87", "-out", "private.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["openssl", "pkey", "-in", "private.key", "-pubout", "-out", "public.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# SLH-DSA (FIPS 205) - Digital Signatures
def generate_SLH_DSA_SHA2_128s_keys():
    """Generate SLH-DSA-SHA2-128s key pair"""
    subprocess.run(["openssl", "genpkey", "-algorithm", "SLH-DSA-SHA2-128s", "-out", "private.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["openssl", "pkey", "-in", "private.key", "-pubout", "-out", "public.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def generate_SLH_DSA_SHA2_128f_keys():
    """Generate SLH-DSA-SHA2-128f key pair"""
    subprocess.run(["openssl", "genpkey", "-algorithm", "SLH-DSA-SHA2-128f", "-out", "private.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["openssl", "pkey", "-in", "private.key", "-pubout", "-out", "public.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def generate_SLH_DSA_SHAKE_128s_keys():
    """Generate SLH-DSA-SHAKE-128s key pair"""
    subprocess.run(["openssl", "genpkey", "-algorithm", "SLH-DSA-SHAKE-128s", "-out", "private.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["openssl", "pkey", "-in", "private.key", "-pubout", "-out", "public.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# SLH-DSA 192 and 256 (FIPS 205) - Digital Signatures
def generate_SLH_DSA_SHA2_192s_keys():
    """Generate SLH-DSA-SHA2-192s key pair"""
    subprocess.run(["openssl", "genpkey", "-algorithm", "SLH-DSA-SHA2-192s", "-out", "private.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["openssl", "pkey", "-in", "private.key", "-pubout", "-out", "public.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def generate_SLH_DSA_SHA2_192f_keys():
    """Generate SLH-DSA-SHA2-192f key pair"""
    subprocess.run(["openssl", "genpkey", "-algorithm", "SLH-DSA-SHA2-192f", "-out", "private.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["openssl", "pkey", "-in", "private.key", "-pubout", "-out", "public.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def generate_SLH_DSA_SHAKE_192s_keys():
    """Generate SLH-DSA-SHAKE-192s key pair"""
    subprocess.run(["openssl", "genpkey", "-algorithm", "SLH-DSA-SHAKE-192s", "-out", "private.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["openssl", "pkey", "-in", "private.key", "-pubout", "-out", "public.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def generate_SLH_DSA_SHA2_256s_keys():
    """Generate SLH-DSA-SHA2-256s key pair"""
    subprocess.run(["openssl", "genpkey", "-algorithm", "SLH-DSA-SHA2-256s", "-out", "private.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["openssl", "pkey", "-in", "private.key", "-pubout", "-out", "public.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def generate_SLH_DSA_SHA2_256f_keys():
    """Generate SLH-DSA-SHA2-256f key pair"""
    subprocess.run(["openssl", "genpkey", "-algorithm", "SLH-DSA-SHA2-256f", "-out", "private.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["openssl", "pkey", "-in", "private.key", "-pubout", "-out", "public.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def generate_SLH_DSA_SHAKE_256s_keys():
    """Generate SLH-DSA-SHAKE-256s key pair"""
    subprocess.run(["openssl", "genpkey", "-algorithm", "SLH-DSA-SHAKE-256s", "-out", "private.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["openssl", "pkey", "-in", "private.key", "-pubout", "-out", "public.key"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ── Key Generation Settings ──────────────────────────────────────────────────


algorithms = [
    ("RSA-2048", generate_RSA_keys),
    ("ECDH P-256", generate_ECDH_keys), 
    ("X25519", generate_X25519_keys),
    ("ECDSA P-256", generate_ECDSA_keys),
    ("ML-KEM-512", generate_ML_KEM_512_keys),
    ("ML-KEM-768", generate_ML_KEM_768_keys),
    ("ML-KEM-1024", generate_ML_KEM_1024_keys),
    ("ML-DSA-44", generate_ML_DSA_44_keys),
    ("ML-DSA-65", generate_ML_DSA_65_keys),
    ("ML-DSA-87", generate_ML_DSA_87_keys),
    ("SLH-DSA-SHA2-128s", generate_SLH_DSA_SHA2_128s_keys),
    ("SLH-DSA-SHA2-128f", generate_SLH_DSA_SHA2_128f_keys),
    ("SLH-DSA-SHAKE-128s", generate_SLH_DSA_SHAKE_128s_keys),
    ("SLH-DSA-SHA2-192s", generate_SLH_DSA_SHA2_192s_keys),
    ("SLH-DSA-SHA2-192f", generate_SLH_DSA_SHA2_192f_keys),
    ("SLH-DSA-SHAKE-192s", generate_SLH_DSA_SHAKE_192s_keys),
    ("SLH-DSA-SHA2-256s", generate_SLH_DSA_SHA2_256s_keys),
    ("SLH-DSA-SHA2-256f", generate_SLH_DSA_SHA2_256f_keys),
    ("SLH-DSA-SHAKE-256s", generate_SLH_DSA_SHAKE_256s_keys)
]

print("Available algorithms:")
for i, (name, _) in enumerate(algorithms, 1):
        print(f"{i}. {name}")

selected_algorithm = input("Enter the number of the algorithm to benchmark: ")
number_of_keys = int(input("Enter the number of keys generated per algorithm: "))
print(f"Generating {number_of_keys} keys for {algorithms[int(selected_algorithm) - 1][0]}.")
results.append(f"Generating {number_of_keys} keys for {algorithms[int(selected_algorithm) - 1][0]}.")

time_start = time.time()
for i in range(number_of_keys):
    algorithms[int(selected_algorithm) - 1][1]()
time_end = time.time()
total_time = time_end - time_start
print(f"Total time taken to generate {number_of_keys} keys: {total_time:.6f} seconds")
results.append(f"Total time taken to generate {number_of_keys} keys: {total_time:.6f} seconds")
baseline_wattage = float(input("Enter the baseline wattage (W): "))
on_load_wattage = float(input("Enter the on-load wattage (W): "))
power_consumption = total_time * (on_load_wattage - baseline_wattage)
print(f"Estimated power consumption for {number_of_keys} keys: {power_consumption:.6f} watt-seconds (Joules)")
results.append(f"Estimated power consumption for {number_of_keys} keys: {power_consumption:.6f} watt-seconds (Joules)")
print("Estimated power consumption per key: {:.6f} watt-seconds (Joules)".format(power_consumption / number_of_keys))
results.append("Estimated power consumption per key: {:.6f} watt-seconds (Joules)".format(power_consumption / number_of_keys))
print("Estimated number of keys generated per watt-second: {:.6f}".format(number_of_keys / power_consumption))
results.append("Estimated number of keys generated per watt-second: {:.6f}".format(number_of_keys / power_consumption))


with open(filename, "w") as f:
    for line in results:
        print(line)
        f.write(line + "\n")

print(f"\nResults saved to {filename}")