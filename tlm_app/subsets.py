"""
Database column name grouping to parse and plot LTU telemetry
"""

sets = {
    "brd": ["cutime", "brd_lt1", "brd_lt2", "brd_lt3", "brd_lt4"],
    "ldd_lt": ["cutime", "ldd_lt1", "ldd_lt2", "ldd_lt3"],
    "ldd_rt": ["cutime", "ldd_rt1", "ldd_rt2", "ldd_rt3"],
    "ldd_volt": ["cutime", "ldd_hv1", "ldd_ldout1"],
    "pls_hv": ["cutime", "pls_hvr1", "pls_hvr2", "pls_hvf1", "pls_hvr2"],
    "pls_ld": ["cutime", "pls_ldr1", "pls_ldr2", "pls_ldf1", "pls_ldf2"],
    "pls_cur": ["cutime", "pls_i1", "pls_i2", "pls_i3", "pls_i4"],
    "chg_cur": ["cutime", "chg_vtcur1", "chg_vscur"],
    "chg_volt": ["cutime", "chg_vsdiv", "chg_vtdiv1"],
}
