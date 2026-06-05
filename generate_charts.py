# Visualisation script generated with GitHub Copilot assistance, May 2026

import csv
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------------------
# Output directory
# ---------------------------------------------------------------------------
CHARTS_DIR = 'charts'
os.makedirs(CHARTS_DIR, exist_ok=True)

plt.style.use('seaborn-v0_8-whitegrid')
DPI = 150

# ---------------------------------------------------------------------------
# Data-loading helpers
# ---------------------------------------------------------------------------

def load_results_csv(filepath='results.csv'):
    """Return a list of row dicts from results.csv, skipping blank rows."""
    rows = []
    with open(filepath, newline='', encoding='utf-8-sig') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            if row.get('machine', '').strip():
                rows.append(row)
    return rows


def load_joules_per_iteration(filepath='joules_per_iteration.csv'):
    """Parse joules_per_iteration.csv.

    Returns two dicts:
        keys_data    – {algo: {machine: value}}
        signing_data – {algo: {machine: value}}
    """
    keys_data = {}
    signing_data = {}
    current_section = None
    machines = []

    with open(filepath, newline='', encoding='utf-8-sig') as fh:
        reader = csv.reader(fh)
        for row in reader:
            if not any(cell.strip() for cell in row):
                continue
            first = row[0].strip()
            if first == 'Keys':
                current_section = 'Keys'
                machines = [m.strip() for m in row[1:] if m.strip()]
                continue
            if first == 'Signing':
                current_section = 'Signing'
                machines = [m.strip() for m in row[1:] if m.strip()]
                continue
            if current_section and machines and first:
                values = {}
                for i, machine in enumerate(machines):
                    try:
                        values[machine] = float(row[i + 1])
                    except (ValueError, IndexError):
                        values[machine] = None
                if current_section == 'Keys':
                    keys_data[first] = values
                else:
                    signing_data[first] = values
    return keys_data, signing_data


# ---------------------------------------------------------------------------
# Pretty display names
# ---------------------------------------------------------------------------
MACHINE_LABELS = {
    'pi1':            'Pi 1',
    'pizero':         'Pi Zero',
    'pi2':            'Pi 2\n(32-bit)',
    'pi2b':           'Pi 2\n(64-bit)',
    'pizero2':        'Pi Zero 2',
    'pi3':            'Pi 3',
    'pi4':            'Pi 4',
    'MacBookAir':     'MacBook Air',
    'Thinkpad-Intel': 'ThinkPad\nIntel',
    'Thinkpad-AMD':   'ThinkPad\nAMD',
}


def _bar_positions(n_groups, n_bars, bar_width=0.15, gap=0.05):
    """Return (group_centres, offsets_per_bar) for a grouped bar chart."""
    total_width = n_bars * bar_width + gap
    centres = np.arange(n_groups) * total_width
    offsets = [(i - (n_bars - 1) / 2) * bar_width for i in range(n_bars)]
    return centres, offsets


# ---------------------------------------------------------------------------
# Chart 1 – Signing Energy Cost per Iteration (Log Scale)
# ---------------------------------------------------------------------------
def chart_01_signing_energy_log():
    _, signing = load_joules_per_iteration()

    machines_order = ['pi1', 'pizero', 'pi2', 'pi2b', 'pizero2', 'pi3', 'pi4']
    algos_order = [
        'ecdsa',
        'ml-dsa-44',
        'slh-dsa-sha2-128f',
        'slh-dsa-sha2-128s',
        'slh-dsa-shake-192s',
    ]
    algo_labels = {
        'ecdsa':              'ECDSA',
        'ml-dsa-44':          'ML-DSA-44',
        'slh-dsa-sha2-128f':  'SLH-DSA-SHA2-128f',
        'slh-dsa-sha2-128s':  'SLH-DSA-SHA2-128s',
        'slh-dsa-shake-192s': 'SLH-DSA-SHAKE-192s',
    }

    n_groups = len(machines_order)
    n_bars = len(algos_order)
    bar_width = 0.14
    centres, offsets = _bar_positions(n_groups, n_bars, bar_width=bar_width)
    colours = plt.cm.tab10.colors[:n_bars]

    fig, ax = plt.subplots(figsize=(12, 6))
    for idx, algo in enumerate(algos_order):
        values = [signing[algo].get(m) for m in machines_order]
        positions = centres + offsets[idx]
        ax.bar(positions, values, width=bar_width, label=algo_labels[algo],
               color=colours[idx], edgecolor='white', linewidth=0.5)

    ax.set_yscale('log')
    ax.set_xticks(centres)
    ax.set_xticklabels([MACHINE_LABELS[m] for m in machines_order], fontsize=10)
    ax.set_xlabel('Machine', fontsize=12)
    ax.set_ylabel('Joules per iteration (log scale)', fontsize=12)
    ax.set_title('Signing Energy Cost per Iteration by Machine (Log Scale)', fontsize=13)
    ax.legend(fontsize=9, loc='upper right')
    plt.tight_layout()
    out = os.path.join(CHARTS_DIR, '01_signing_energy_log.png')
    plt.savefig(out, dpi=DPI)
    plt.close()
    print(f'Saved: {out}')


# ---------------------------------------------------------------------------
# Chart 3 – Key Generation Time (KEMs)
# ---------------------------------------------------------------------------
def chart_03_kem_feasibility_time():
    results = load_results_csv()

    machines_order = ['pi1', 'pizero', 'pi2', 'pi2b', 'pizero2', 'pi3', 'pi4']
    algos_order = ['ECDH P-256', 'X25519', 'ML-KEM-512', 'ML-KEM-768', 'ML-KEM-1024']

    lookup = {}
    for row in results:
        if row['method'] != 'key generation':
            continue
        m = row['machine']
        a = row['algorithm']
        if m in machines_order and a in algos_order:
            lookup.setdefault(m, {})[a] = float(row['time per iteration'])

    n_groups = len(machines_order)
    n_bars = len(algos_order)
    bar_width = 0.12
    centres, offsets = _bar_positions(n_groups, n_bars, bar_width=bar_width)
    colours = plt.cm.tab10.colors[:n_bars]

    fig, ax = plt.subplots(figsize=(13, 6))
    for idx, algo in enumerate(algos_order):
        values = [lookup.get(m, {}).get(algo) for m in machines_order]
        positions = centres + offsets[idx]
        ax.bar(positions, values, width=bar_width, label=algo,
               color=colours[idx], edgecolor='white', linewidth=0.5)

    ax.set_xticks(centres)
    ax.set_xticklabels([MACHINE_LABELS[m] for m in machines_order], fontsize=10)
    ax.set_xlabel('Machine', fontsize=12)
    ax.set_ylabel('Time per iteration (seconds)', fontsize=12)
    ax.set_title('Key Generation Time per Iteration — Classical vs PQC KEMs', fontsize=13)
    ax.legend(fontsize=9, loc='upper right')
    plt.tight_layout()
    out = os.path.join(CHARTS_DIR, '03_kem_feasibility_time.png')
    plt.savefig(out, dpi=DPI)
    plt.close()
    print(f'Saved: {out}')


# ---------------------------------------------------------------------------
# Chart 7 – ML-KEM Energy Efficiency: Why Faster is Better
# ---------------------------------------------------------------------------
def chart_07_mlkem_energy_efficiency():
    """
    Data sourced directly from results.csv (ML-KEM-768, key generation).
    Joules = joules_per_iteration x 100.
    """

    machines_order = ['pizero', 'pi1', 'pi2', 'pi2b', 'pizero2', 'pi3', 'pi4']
    display_names  = ['Pi Zero', 'Pi 1', 'Pi 2\n(32-bit)', 'Pi 2\n(64-bit)',
                      'Pi Zero 2', 'Pi 3', 'Pi 4']

    joules_100 = {
        'pizero':  0.049994217 * 100,
        'pi1':     0.050223016 * 100,
        'pi2':     0.041849514 * 100,
        'pi2b':    0.035639249 * 100,
        'pizero2': 0.038845593 * 100,
        'pi3':     0.043442313 * 100,
        'pi4':     0.035161105 * 100,
    }

    joules_values = [joules_100[m] for m in machines_order]

    fig, ax = plt.subplots(figsize=(13, 7))

    bars = ax.bar(range(len(machines_order)), joules_values, width=0.6,
                  label='Energy Used — 100 iterations (Joules)',
                  color='#2E86AB', alpha=0.85, edgecolor='white', linewidth=1.5)

    ax.yaxis.grid(True, alpha=0.2, linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Machine', fontsize=12, fontweight='bold')
    ax.set_ylabel('Energy for 100 ML-KEM-768 Key-Gen operations (Joules)',
                  fontsize=11, fontweight='bold', color='#2E86AB')
    ax.tick_params(axis='y', labelcolor='#2E86AB')
    ax.set_xticks(range(len(machines_order)))
    ax.set_xticklabels(display_names, fontsize=11)

    for bar, val in zip(bars, joules_values):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.05,
                f'{val:.2f} J', ha='center', va='bottom',
                fontsize=9, fontweight='bold', color='#2E86AB')

    ax.set_title(
        'ML-KEM-768 Key Generation — Energy for 100 Operations',
        fontsize=13, fontweight='bold', pad=20)

    plt.tight_layout()
    out = os.path.join(CHARTS_DIR, '07_mlkem_energy_efficiency.png')
    plt.savefig(out, dpi=DPI)
    plt.close()
    print(f'Saved: {out}')


# ---------------------------------------------------------------------------
# Chart 8 – SLH-DSA-SHAKE-192s Energy Efficiency
# ---------------------------------------------------------------------------
def chart_08_slh_dsa_energy_efficiency():
    """
    Data sourced directly from results.csv (SLH-DSA-SHAKE-192s, signatures).
    Joules = joules_per_iteration x 100 (extrapolated where only 10 iters run).
    """

    machines_order = ['pizero', 'pi1', 'pi2', 'pi2b', 'pizero2', 'pi3', 'pi4']
    display_names  = ['Pi Zero', 'Pi 1', 'Pi 2\n(32-bit)', 'Pi 2\n(64-bit)',
                      'Pi Zero 2', 'Pi 3', 'Pi 4']

    joules_100 = {
        'pizero':  24.76296897  * 100,
        'pi1':     18.76015142  * 100,
        'pi2':     19.65578286  * 100,
        'pi2b':     5.730838546 * 100,
        'pizero2':  6.528834304 * 100,
        'pi3':      7.374940633 * 100,
        'pi4':      5.471396597 * 100,
    }

    joules_values = [joules_100[m] for m in machines_order]

    fig, ax = plt.subplots(figsize=(13, 7))

    bars = ax.bar(range(len(machines_order)), joules_values, width=0.6,
                  label='Energy Used — 100 iterations (Joules)',
                  color='#C44E52', alpha=0.85, edgecolor='white', linewidth=1.5)

    ax.yaxis.grid(True, alpha=0.2, linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Machine', fontsize=12, fontweight='bold')
    ax.set_ylabel('Energy for 100 SLH-DSA-SHAKE-192s Signing operations (Joules)',
                  fontsize=11, fontweight='bold', color='#C44E52')
    ax.tick_params(axis='y', labelcolor='#C44E52')
    ax.set_xticks(range(len(machines_order)))
    ax.set_xticklabels(display_names, fontsize=11)

    for bar, val in zip(bars, joules_values):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 20,
                f'{val:.0f} J', ha='center', va='bottom',
                fontsize=9, fontweight='bold', color='#C44E52')

    ax.set_title(
        'SLH-DSA-SHAKE-192s Signing — Energy for 100 Operations\n'
        '(extrapolated to 100 iterations where fewer were run)',
        fontsize=13, fontweight='bold', pad=20)

    plt.tight_layout()
    out = os.path.join(CHARTS_DIR, '08_slh_dsa_shake_192s_energy.png')
    plt.savefig(out, dpi=DPI)
    plt.close()
    print(f'Saved: {out}')

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    chart_01_signing_energy_log()
    chart_03_kem_feasibility_time()
    chart_07_mlkem_energy_efficiency()
    chart_08_slh_dsa_energy_efficiency()