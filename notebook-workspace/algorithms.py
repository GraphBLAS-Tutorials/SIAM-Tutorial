import pygraphblas as grb

#==========================================================================
def neighborhood(graph, src, num_hops):
    num_nodes = graph.nrows
    w = grb.Vector.sparse(grb.types.BOOL, num_nodes)
    v = grb.Vector.sparse(grb.types.BOOL, num_nodes)
    w[src] = True
    v.assign_scalar(True, mask=w)

    with grb.BOOL.LOR_LAND:
        for it in range(num_hops):
            w.vxm(graph, mask=v, out=w, desc=grb.descriptor.RC)
            v.assign_scalar(True, mask=w)

    return v

#==========================================================================
def pagerank(A, damping = 0.85, itermax = 100):
    d = A.reduce_vector(grb.types.FP32.PLUS_MONOID)

    n = A.nrows
    r = grb.Vector.sparse(grb.types.FP32, n)
    t = grb.Vector.sparse(grb.types.FP32, n)
    d.assign_scalar(damping, accum=grb.types.FP32.DIV)
    r[:] = 1.0 / n
    teleport = (1 - damping) / n
    tol = 1e-4
    rdiff = 1.0
    for i in range(itermax):
        # swap t and r
        temp = t ; t = r ; r = temp
        w = t / d
        r[:] = teleport
        A.mxv(w,
              out=r,
              accum=grb.types.FP32.PLUS,
              semiring=grb.types.FP32.PLUS_SECOND,
              desc=grb.descriptor.T0)
        t -= r
        t.apply(grb.types.FP32.ABS, out=t)
        rdiff = t.reduce_float()
        if rdiff <= tol:
            break
    return r
