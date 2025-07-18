GC_FAULT_METADATA = {
    "Tailing": {
        "Cause": "Active sites in inlet/column or contamination",
        "Fix": "Replace liner, check septa/ferrules, bake column"
    },
    "Fronting": {
        "Cause": "Overloading or flow issues",
        "Fix": "Dilute sample, check inlet pressure, reduce split ratio"
    },
    "Signal Loss": {
        "Cause": "FID flame out, TCD filament issue, leak",
        "Fix": "Reignite detector, check for leaks or flow loss"
    },
    "Ghost Peaks": {
        "Cause": "Carryover or dirty injector",
        "Fix": "Clean injector, purge autosampler, run blank"
    },
    "Baseline Drift": {
        "Cause": "Column bleed, EPC fluctuation, oven temp instability",
        "Fix": "Check oven and EPC stability, condition column"
    },
    "Negative Peaks": {
        "Cause": "TCD polarity or subtraction issue",
        "Fix": "Check signal polarity and subtraction logic"
    },
    "Catalyst Loss": {
        "Cause": "Methanizer catalyst degradation",
        "Fix": "Replace or regenerate catalyst"
    },
    "Plasma Disruption": {
        "Cause": "SCD dual burner issue or plasma extinguish",
        "Fix": "Check gas flows, clean burner, verify dual burn stability"
    },
    "No Ignition": {
        "Cause": "FID ignition failed or flame blew out",
        "Fix": "Reignite manually, check hydrogen/air flow"
    },
    "Flame Blowout Mid-run": {
        "Cause": "Sudden pressure/flow disruption",
        "Fix": "Check column leaks, hydrogen/air flow"
    },
    "Injector Leak": {
        "Cause": "Worn septa or loose fitting",
        "Fix": "Replace septa, tighten fittings"
    }
}
