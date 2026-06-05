# This programs benchmarks the key generation times for various classical and post-quantum 
# cryptographic algorithms using OpenSSL's command-line tools. 
# It runs each key generation function multiple times, measures the average time taken, 
# and saves the results to a timestamped text file named after the machine.
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

ITERATIONS = int(input("Enter the number of keys generated per algorithm (Default 100): ") or 100)

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

# ── Benchmark Runner ──────────────────────────────────────────────────────────

def benchmark(label, fn, iterations=ITERATIONS):
    print(f"Benchmarking {label}...")
    start = time.time()
    for _ in range(iterations):
        fn()
    end = time.time()
    avg = (end - start) / iterations
    result = f"{label}: {avg:.6f}s per operation"
    results.append(result)
    print(result)

# ── Classical Algorithms ──────────────────────────────────────────────────────

results.append("=== Classical Algorithms ===")
benchmark("RSA-2048 keygen",      generate_RSA_keys)
benchmark("ECDH P-256 keygen",    generate_ECDH_keys)
benchmark("X25519 keygen",        generate_X25519_keys)
benchmark("ECDSA P-256 keygen",   generate_ECDSA_keys)

# ── ML-KEM (FIPS 203) ─────────────────────────────────────────────────────────

results.append("")
results.append("=== ML-KEM / CRYSTALS-Kyber (FIPS 203) ===")
benchmark("ML-KEM-512 keygen",    generate_ML_KEM_512_keys)
benchmark("ML-KEM-768 keygen",    generate_ML_KEM_768_keys)
benchmark("ML-KEM-1024 keygen",   generate_ML_KEM_1024_keys)

# ── ML-DSA (FIPS 204) ─────────────────────────────────────────────────────────

results.append("")
results.append("=== ML-DSA / CRYSTALS-Dilithium (FIPS 204) ===")
benchmark("ML-DSA-44 keygen",     generate_ML_DSA_44_keys)
benchmark("ML-DSA-65 keygen",     generate_ML_DSA_65_keys)
benchmark("ML-DSA-87 keygen",     generate_ML_DSA_87_keys)

# ── SLH-DSA (FIPS 205) ───────────────────────────────────────────────────────


results.append("")
results.append("=== SLH-DSA / SPHINCS+ (FIPS 205) ===")
benchmark("SLH-DSA-SHA2-128s keygen",   generate_SLH_DSA_SHA2_128s_keys)
benchmark("SLH-DSA-SHA2-128f keygen",   generate_SLH_DSA_SHA2_128f_keys)
benchmark("SLH-DSA-SHAKE-128s keygen",  generate_SLH_DSA_SHAKE_128s_keys)
benchmark("SLH-DSA-SHA2-192s keygen",   generate_SLH_DSA_SHA2_192s_keys)
benchmark("SLH-DSA-SHA2-192f keygen",   generate_SLH_DSA_SHA2_192f_keys)
benchmark("SLH-DSA-SHAKE-192s keygen",  generate_SLH_DSA_SHAKE_192s_keys)
benchmark("SLH-DSA-SHA2-256s keygen",   generate_SLH_DSA_SHA2_256s_keys)
benchmark("SLH-DSA-SHA2-256f keygen",   generate_SLH_DSA_SHA2_256f_keys)
benchmark("SLH-DSA-SHAKE-256s keygen",  generate_SLH_DSA_SHAKE_256s_keys)

# ── Write Results ─────────────────────────────────────────────────────────────

results.append("")
results.append("Done!")

with open(filename, "w") as f:
    for line in results:
        print(line)
        f.write(line + "\n")

print(f"\nResults saved to {filename}")
