# The PQC Benchmark
# This is the implementation of my Post Quantum Cryptography benchmark, which measures the performance of 
# various post-quantum algorithms in key generation, signing, verification, and TLS handshakes. 
# The benchmark is designed to be run on a local machine and outputs results to a CSV file for analysis.
#
# After benchmarking all the machines, it appears that TLS handshakes are not functioning correctly.
# I am leaving the code in place for now, to allow for future debugging.
#
# Key generation and signature operations are working as expected, and the results are being recorded in the CSV file.
#
# OG 
import subprocess
import os
import csv
import datetime
import time
import platform

#----------------Initialisation------------------
# Get machine name and create timestamp
machine_name = platform.node()
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
# Initialise results CSV file with timestamped name and header
# Ensure results_files directory exists
os.makedirs("results_files", exist_ok=True)
csv_file = os.path.join("results_files", f"{machine_name}_{timestamp}.csv")
csv_header = [
    "machine", "method", "submethod", "algorithm", "iterations", "start time", "stop time", "total time",
    "time per iteration", "baseline power", "on-load power", "total power used",
    "joules per iteration", "iterations per joule"
]
# Create the CSV file and write header
with open(csv_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(csv_header)

# Helper function to append a row to the CSV
def append_result_row(row):
    with open(csv_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)

# Key generation function
def gen_key(command, args, priv, pub):
    # Replace {priv} in args with the actual priv path
    args = [a.replace("{priv}", priv) for a in args]
    # Generate private key
    subprocess.run(["openssl", command] + args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Output public key
    subprocess.run(["openssl", "pkey", "-in", priv, "-pubout", "-out", pub], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Signing function
def sign_file(private_key, message_to_sign, signature):
    # Sign a file using a private key.
    # Uses OpenSSL's pkeyutl utility to sign the input file with the given private key.
    # The signature is written to signature_output. All output is suppressed.
    return subprocess.run([
        "openssl", "pkeyutl",
        "-sign",
        "-inkey", private_key,
        "-in", message_to_sign,
        "-out", signature
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Verification function
def verify_signature(public_key, message_to_sign, signature):
    # Verify a signature using a public key.
    # Uses OpenSSL's pkeyutl utility to verify the signature of the input file with the given public key.
    # Returns True if the signature is valid, False otherwise. All output is suppressed.
    result = subprocess.run([
        "openssl", "pkeyutl",
        "-verify",
        "-pubin",
        "-inkey", public_key,
        "-in", message_to_sign,
        "-sigfile", signature
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

# TLS certificate generation function
def gen_tls_cert(command, args, priv, cert):
    # Generate private key
    args_with_priv = [a.replace("{priv}", priv) for a in args]
    subprocess.run(["openssl", command] + args_with_priv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Generate self-signed certificate valid for 365 days
    subprocess.run([
        "openssl", "req", "-new", "-x509", "-key", priv, "-out", cert,
        "-days", "365", "-subj", "/CN=localhost"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# TLS handshake benchmarking function
def benchmark_tls_handshake(cert, priv, iterations, port=4433):
    # Start s_server in background
    server_proc = subprocess.Popen([
        "openssl", "s_server",
        "-cert", cert,
        "-key", priv,
        "-accept", str(port),
        "-quiet"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Give the server a moment to start
    time.sleep(0.5)
    
    # Run client handshakes and measure time
    time_start = time.time()
    for i in range(iterations):
        subprocess.run([
            "openssl", "s_client",
            "-connect", f"localhost:{port}",
            "-brief"
        ], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time_end = time.time()
    
    # Stop the server
    server_proc.terminate()
    server_proc.wait(timeout=5)
    
    return time_end - time_start

while True:
    choice = input("Press y to start, x to exit: ")
    if choice.lower() == 'x':
        break
    elif choice.lower() == 'y':
        pass
    else:
        print("Invalid choice. Please try again.")

    methods = ["key generation", "signatures", "TLS handshake"]
    chosenMethod = int(input("Select a method to benchmark:\n" + "\n".join(f"{i}. {m}" for i, m in enumerate(methods)) + "\nEnter number: "))
    if chosenMethod == 0:

        keygen_algorithms = [
            ("RSA-2048", "genrsa", ["-out", "{priv}", "2048"]),
            ("ECDSA P-256", "genpkey", ["-algorithm", "EC", "-pkeyopt", "ec_paramgen_curve:P-256", "-out", "{priv}"]),
            ("X25519", "genpkey", ["-algorithm", "X25519", "-out", "{priv}"]),
            ("ECDH P-256", "genpkey", ["-algorithm", "EC", "-pkeyopt", "ec_paramgen_curve:P-256", "-out", "{priv}"]),
            ("ML-KEM-512", "genpkey", ["-algorithm", "ML-KEM-512", "-out", "{priv}"]),
            ("ML-KEM-768", "genpkey", ["-algorithm", "ML-KEM-768", "-out", "{priv}"]),
            ("ML-KEM-1024", "genpkey", ["-algorithm", "ML-KEM-1024", "-out", "{priv}"]),
            ("ML-DSA-44", "genpkey", ["-algorithm", "ML-DSA-44", "-out", "{priv}"]),
            ("ML-DSA-65", "genpkey", ["-algorithm", "ML-DSA-65", "-out", "{priv}"]),
            ("ML-DSA-87", "genpkey", ["-algorithm", "ML-DSA-87", "-out", "{priv}"]),
            ("SLH-DSA-SHA2-128s", "genpkey", ["-algorithm", "SLH-DSA-SHA2-128s", "-out", "{priv}"]),
            ("SLH-DSA-SHA2-128f", "genpkey", ["-algorithm", "SLH-DSA-SHA2-128f", "-out", "{priv}"]),
            ("SLH-DSA-SHAKE-128s", "genpkey", ["-algorithm", "SLH-DSA-SHAKE-128s", "-out", "{priv}"]),
            ("SLH-DSA-SHA2-192s", "genpkey", ["-algorithm", "SLH-DSA-SHA2-192s", "-out", "{priv}"]),
            ("SLH-DSA-SHA2-192f", "genpkey", ["-algorithm", "SLH-DSA-SHA2-192f", "-out", "{priv}"]),
            ("SLH-DSA-SHAKE-192s", "genpkey", ["-algorithm", "SLH-DSA-SHAKE-192s", "-out", "{priv}"]),
            ("SLH-DSA-SHA2-256s", "genpkey", ["-algorithm", "SLH-DSA-SHA2-256s", "-out", "{priv}"]),
            ("SLH-DSA-SHA2-256f", "genpkey", ["-algorithm", "SLH-DSA-SHA2-256f", "-out", "{priv}"]),
            ("SLH-DSA-SHAKE-256s", "genpkey", ["-algorithm", "SLH-DSA-SHAKE-256s", "-out", "{priv}"]),
        ]

        # Ensure keys directory exists
        os.makedirs("keys", exist_ok=True)

        #1.-------------Key Generation --------------

        #1.a Key generation usage:
        priv = os.path.abspath("/keys/private.key")
        pub = os.path.abspath("/keys/public.key")
        selected = int(input("Select an algorithm to benchmark:\n" + "\n".join(f"{i}. {name}" for i, (name, _, _) in enumerate(keygen_algorithms)) + "\nEnter number: "))
        name, command, args = keygen_algorithms[selected]
        priv = os.path.join("keys", f"{name.replace(' ', '_').replace('-', '_')}_priv.pem")
        pub = os.path.join("keys", f"{name.replace(' ', '_').replace('-', '_')}_pub.pem")

        iterations = int(input("Enter the number of iterations for key generation: "))
        time_start = time.time()
        for i in range(iterations):
            gen_key(command, args, priv, pub)
        time_end = time.time()
        total_time = time_end - time_start
        time_per_iteration = total_time / iterations
        power_metrics = input("Enter power metrics (baseline power, on-load power) separated by commas (or leave blank): ")
        if power_metrics.strip():
            baseline_power, on_load_power = (power_metrics.split(",") + ["", ""])[:2]
            baseline_power = baseline_power.strip()
            on_load_power = on_load_power.strip()
            total_power = float(on_load_power) - float(baseline_power) if baseline_power and on_load_power else ""
            joules_per_iteration = float(total_power) * time_per_iteration if total_power and time_per_iteration else ""
            iterations_per_joule = iterations / (float(total_power) * total_time) if total_power and total_time else ""
            append_result_row([machine_name, methods[chosenMethod], "", keygen_algorithms[selected][0], iterations, time_start, time_end, total_time, time_per_iteration, baseline_power, on_load_power, total_power, joules_per_iteration, iterations_per_joule])
        else:
            baseline_power, on_load_power, total_power, joules_per_iteration, iterations_per_joule = "", "", "", "", ""
            append_result_row([machine_name, methods[chosenMethod], "", keygen_algorithms[selected][0], iterations, time_start, time_end, total_time, time_per_iteration, baseline_power, on_load_power, total_power, joules_per_iteration, iterations_per_joule])

        
    # 2------------------Signing------------------
    elif chosenMethod == 1:
        signature_algorithms = [
            ("RSA-2048", "genrsa", ["-out", "{priv}", "2048"]),
            ("ECDSA P-256", "genpkey", ["-algorithm", "EC", "-pkeyopt", "ec_paramgen_curve:P-256", "-out", "{priv}"]),
            ("ML-DSA-44", "genpkey", ["-algorithm", "ML-DSA-44", "-out", "{priv}"]),
            ("ML-DSA-65", "genpkey", ["-algorithm", "ML-DSA-65", "-out", "{priv}"]),
            ("ML-DSA-87", "genpkey", ["-algorithm", "ML-DSA-87", "-out", "{priv}"]),
            ("SLH-DSA-SHA2-128s", "genpkey", ["-algorithm", "SLH-DSA-SHA2-128s", "-out", "{priv}"]),
            ("SLH-DSA-SHA2-128f", "genpkey", ["-algorithm", "SLH-DSA-SHA2-128f", "-out", "{priv}"]),
            ("SLH-DSA-SHAKE-128s", "genpkey", ["-algorithm", "SLH-DSA-SHAKE-128s", "-out", "{priv}"]),
            ("SLH-DSA-SHA2-192s", "genpkey", ["-algorithm", "SLH-DSA-SHA2-192s", "-out", "{priv}"]),
            ("SLH-DSA-SHA2-192f", "genpkey", ["-algorithm", "SLH-DSA-SHA2-192f", "-out", "{priv}"]),
            ("SLH-DSA-SHAKE-192s", "genpkey", ["-algorithm", "SLH-DSA-SHAKE-192s", "-out", "{priv}"]),
            ("SLH-DSA-SHA2-256s", "genpkey", ["-algorithm", "SLH-DSA-SHA2-256s", "-out", "{priv}"]),
            ("SLH-DSA-SHA2-256f", "genpkey", ["-algorithm", "SLH-DSA-SHA2-256f", "-out", "{priv}"]),
            ("SLH-DSA-SHAKE-256s", "genpkey", ["-algorithm", "SLH-DSA-SHAKE-256s", "-out", "{priv}"]),
        ]
        
        # Generate the keys for the signature algorithms

        priv = os.path.abspath("/keys/private.key")
        pub = os.path.abspath("/keys/public.key")
        selected = int(input("Select an algorithm to benchmark:\n" + "\n".join(f"{i}. {name}" for i, (name, _, _) in enumerate(signature_algorithms)) + "\nEnter number: "))
        name, command, args = signature_algorithms[selected]
        priv = os.path.join("keys", f"{name.replace(' ', '_').replace('-', '_')}_priv.pem")
        pub = os.path.join("keys", f"{name.replace(' ', '_').replace('-', '_')}_pub.pem")
        gen_key(command, args, priv, pub)

        signature_methods = ["signing", "verification"]
        selected_method = int(input("Select a signature method to benchmark:\n" + "\n".join(f"{i}. {m}" for i, m in enumerate(signature_methods)) + "\nEnter number: "))

        # Sign a message 
        if not os.path.exists("README.md"):
            with open("README.md", "w") as f:
                f.write("This is a sample file for signature benchmarking.\n")
        message_to_sign = "README.md"
        private_key = priv
        signature_output = os.path.join("signatures", f"{name.replace(' ', '_').replace('-', '_')}_signature.bin")
        os.makedirs("signatures", exist_ok=True)

        if selected_method == 0:
            iterations = int(input("Enter the number of iterations for signing: "))
            time_start = time.time()
            for i in range(iterations):
                sign_file(private_key, message_to_sign, signature_output)
            time_end = time.time()
            total_time = time_end - time_start
            time_per_iteration = total_time / iterations if iterations else 0
            power_metrics = input("Enter power metrics (baseline power, on-load power) separated by commas (or leave blank): ")
            if power_metrics.strip():
                baseline_power, on_load_power = (power_metrics.split(",") + ["", ""])[:2]
                baseline_power = baseline_power.strip()
                on_load_power = on_load_power.strip()
                total_power = float(on_load_power) - float(baseline_power) if baseline_power and on_load_power else ""
                joules_per_iteration = float(total_power) * time_per_iteration if total_power and time_per_iteration else ""
                iterations_per_joule = iterations / (float(total_power) * total_time) if total_power and total_time else ""
                append_result_row([machine_name, methods[chosenMethod], signature_methods[selected_method], signature_algorithms[selected][0], iterations, time_start, time_end, total_time, time_per_iteration, baseline_power, on_load_power, total_power, joules_per_iteration, iterations_per_joule])
            else:
                baseline_power, on_load_power, total_power, joules_per_iteration, iterations_per_joule = "", "", "", "", ""
                append_result_row([machine_name, methods[chosenMethod], signature_methods[selected_method], signature_algorithms[selected][0], iterations, time_start, time_end, total_time, time_per_iteration, baseline_power, on_load_power, total_power, joules_per_iteration, iterations_per_joule])

        elif selected_method == 1:
            # Create a signature first to verify
            sign_file(private_key, message_to_sign, signature_output)
            
            # Verify the signature
            public_key = pub
            iterations = int(input("Enter the number of iterations for signature verification: "))
            time_start = time.time()
            for i in range(iterations):
                verify_signature(public_key, message_to_sign, signature_output)
            time_end = time.time()
            total_time = time_end - time_start
            time_per_iteration = total_time / iterations if iterations else 0
            power_metrics = input("Enter power metrics (baseline power, on-load power) separated by commas (or leave blank): ")
            if power_metrics.strip():
                baseline_power, on_load_power = (power_metrics.split(",") + ["", ""])[:2]
                baseline_power = baseline_power.strip()
                on_load_power = on_load_power.strip()
                total_power = float(on_load_power) - float(baseline_power) if baseline_power and on_load_power else ""
                joules_per_iteration = float(total_power) * time_per_iteration if total_power and time_per_iteration else ""
                iterations_per_joule = iterations / (float(total_power) * total_time) if total_power and total_time else ""
                append_result_row([machine_name, methods[chosenMethod], signature_methods[selected_method], signature_algorithms[selected][0], iterations, time_start, time_end, total_time, time_per_iteration, baseline_power, on_load_power, total_power, joules_per_iteration, iterations_per_joule])
            else:
                baseline_power, on_load_power, total_power, joules_per_iteration, iterations_per_joule = "", "", "", "", ""
                append_result_row([machine_name, methods[chosenMethod], signature_methods[selected_method], signature_algorithms[selected][0], iterations, time_start, time_end, total_time, time_per_iteration, baseline_power, on_load_power, total_power, joules_per_iteration, iterations_per_joule])

        #3------------------TLS handshake------------------
    elif chosenMethod == 2:
        tls_algorithms = [
            ("RSA-2048", "genrsa", ["-out", "{priv}", "2048"]),
            ("ECDSA P-256", "genpkey", ["-algorithm", "EC", "-pkeyopt", "ec_paramgen_curve:P-256", "-out", "{priv}"]),
            ("ML-DSA-44", "genpkey", ["-algorithm", "ML-DSA-44", "-out", "{priv}"]),
            ("ML-DSA-65", "genpkey", ["-algorithm", "ML-DSA-65", "-out", "{priv}"]),
            ("ML-DSA-87", "genpkey", ["-algorithm", "ML-DSA-87", "-out", "{priv}"]),
        ]
        
        # Ensure certs directory exists
        os.makedirs("certs", exist_ok=True)
        
        # Select algorithm
        selected = int(input("Select an algorithm to benchmark:\n" + "\n".join(f"{i}. {name}" for i, (name, _, _) in enumerate(tls_algorithms)) + "\nEnter number: "))
        name, command, args = tls_algorithms[selected]
        priv = os.path.join("certs", f"{name.replace(' ', '_').replace('-', '_')}_priv.pem")
        cert = os.path.join("certs", f"{name.replace(' ', '_').replace('-', '_')}_cert.pem")
        
        # Generate certificate
        gen_tls_cert(command, args, priv, cert)
        
        # Get iterations
        iterations = int(input("Enter the number of iterations for TLS handshake: "))
        
        # Run handshakes and measure time
        total_time = benchmark_tls_handshake(cert, priv, iterations)
        time_per_iteration = total_time / iterations
        
        # Get power metrics
        power_metrics = input("Enter power metrics (baseline power, on-load power) separated by commas (or leave blank): ")
        if power_metrics.strip():
            baseline_power, on_load_power = (power_metrics.split(",") + ["", ""])[:2]
            baseline_power = baseline_power.strip()
            on_load_power = on_load_power.strip()
            total_power = float(on_load_power) - float(baseline_power) if baseline_power and on_load_power else ""
            joules_per_iteration = float(total_power) * time_per_iteration if total_power and time_per_iteration else ""
            iterations_per_joule = iterations / (float(total_power) * total_time) if total_power and total_time else ""
            tls_time_start = time.time() - total_time
            tls_time_end = time.time()
            append_result_row([machine_name, methods[chosenMethod], "", tls_algorithms[selected][0], iterations, tls_time_start, tls_time_end, total_time, time_per_iteration, baseline_power, on_load_power, total_power, joules_per_iteration, iterations_per_joule])
        else:
            baseline_power, on_load_power, total_power, joules_per_iteration, iterations_per_joule = "", "", "", "", ""
            tls_time_start = time.time() - total_time
            tls_time_end = time.time()
            append_result_row([machine_name, methods[chosenMethod], "", tls_algorithms[selected][0], iterations, tls_time_start, tls_time_end, total_time, time_per_iteration, baseline_power, on_load_power, total_power, joules_per_iteration, iterations_per_joule])
