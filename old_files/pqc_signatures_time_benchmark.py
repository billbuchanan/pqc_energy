import time
import subprocess
import platform
import datetime
import os
import shutil

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = platform.node() + "_signatures_" + timestamp + ".txt"

results = []
results.append("Machine: " + platform.node())
results.append("Platform: " + platform.machine())
results.append("System: " + platform.system())
results.append("Date: " + timestamp)
results.append("")

README = "README.md"
if not os.path.exists(README):
	raise SystemExit("README.md not found in workspace root")

# --- Key generation functions ---
def run(cmd):
	return subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def gen_rsa_2048(priv):
	run(["openssl", "genrsa", "-out", priv, "2048"])

def gen_ecdsa_p256(priv):
	run(["openssl", "genpkey", "-algorithm", "EC", "-pkeyopt", "ec_paramgen_curve:P-256", "-out", priv])

def gen_generic(alg, priv):
	run(["openssl", "genpkey", "-algorithm", alg, "-out", priv])

# --- Sign / Verify helpers ---
def sign_file(priv, infile, sigout):
	return subprocess.run(["openssl", "pkeyutl", "-sign", "-inkey", priv, "-in", infile, "-out", sigout])

def verify_file(pub, infile, sigfile):
	return subprocess.run(["openssl", "pkeyutl", "-verify", "-pubin", "-inkey", pub, "-in", infile, "-sigfile", sigfile])

def pubout_from_priv(priv, pub):
	# Try generic pkey pubout
	run(["openssl", "pkey", "-in", priv, "-pubout", "-out", pub])

# --- Algorithms to test (signatures only) ---
algorithms = [
	("RSA-2048", lambda p: gen_rsa_2048(p)),
	("ECDSA P-256", lambda p: gen_ecdsa_p256(p)),
	("ML-DSA-44", lambda p: gen_generic("ML-DSA-44", p)),
	("ML-DSA-65", lambda p: gen_generic("ML-DSA-65", p)),
	("ML-DSA-87", lambda p: gen_generic("ML-DSA-87", p)),
	("SLH-DSA-SHA2-128s", lambda p: gen_generic("SLH-DSA-SHA2-128s", p)),
	("SLH-DSA-SHA2-128f", lambda p: gen_generic("SLH-DSA-SHA2-128f", p)),
	("SLH-DSA-SHAKE-128s", lambda p: gen_generic("SLH-DSA-SHAKE-128s", p)),
	("SLH-DSA-SHA2-192s", lambda p: gen_generic("SLH-DSA-SHA2-192s", p)),
	("SLH-DSA-SHA2-192f", lambda p: gen_generic("SLH-DSA-SHA2-192f", p)),
	("SLH-DSA-SHAKE-192s", lambda p: gen_generic("SLH-DSA-SHAKE-192s", p)),
	("SLH-DSA-SHA2-256s", lambda p: gen_generic("SLH-DSA-SHA2-256s", p)),
	("SLH-DSA-SHA2-256f", lambda p: gen_generic("SLH-DSA-SHA2-256f", p)),
	("SLH-DSA-SHAKE-256s", lambda p: gen_generic("SLH-DSA-SHAKE-256s", p)),
]

results.append("=== Signature Algorithms ===")

workdir = os.path.join(os.getcwd(), "pqc_sign_tmp")
os.makedirs(workdir, exist_ok=True)

for name, genfn in algorithms:
	safe = name.replace(' ', '_').replace('/', '_').replace('.', '_').replace('-', '_')
	priv = os.path.join(workdir, safe + "_priv.pem")
	pub = os.path.join(workdir, safe + "_pub.pem")
	sig = os.path.join(workdir, safe + "_sig.bin")

	# Clean old files
	for f in (priv, pub, sig):
		try:
			os.remove(f)
		except OSError:
			pass

	results.append("")
	results.append(f"Algorithm: {name}")

	# Key generation
	t0 = time.time()
	try:
		genfn(priv)
		pubout_from_priv(priv, pub)
		kg_success = os.path.exists(priv) and os.path.exists(pub)
	except Exception as e:
		kg_success = False
		results.append(f"Keygen error: {e}")
	t1 = time.time()
	results.append(f"Keygen success: {kg_success}; time: {t1 - t0:.6f}s")

	if not kg_success:
		continue

	# Sign
	t0 = time.time()
	proc_sig = sign_file(priv, README, sig)
	t1 = time.time()
	sig_ok = (proc_sig.returncode == 0) and os.path.exists(sig)
	results.append(f"Sign success: {sig_ok}; time: {t1 - t0:.6f}s")

	# Verify
	t0 = time.time()
	proc_ver = verify_file(pub, README, sig)
	t1 = time.time()
	ver_ok = (proc_ver.returncode == 0)
	results.append(f"Verify success: {ver_ok}; time: {t1 - t0:.6f}s")

# Cleanup
try:
	shutil.rmtree(workdir)
except OSError:
	pass

results.append("")
results.append("Done!")

with open(filename, "w", encoding="utf-8") as f:
	for line in results:
		print(line)
		f.write(line + "\n")

print(f"\nResults saved to {filename}")

