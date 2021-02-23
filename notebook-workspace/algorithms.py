import pygraphblas as grb

#==========================================================================
def bfs(graph, src_node):
    num_nodes = graph.nrows
    w = grb.Vector.sparse(grb.types.BOOL, num_nodes) #wavefront
    v = grb.Vector.sparse(grb.types.BOOL, num_nodes) #visited
    w[src_node] = True

    with grb.BOOL.LOR_LAND:
        while w.nvals > 0:
            v.assign_scalar(True, mask=w)
            w.vxm(graph, mask=v, out=w, desc=grb.descriptor.RC)

    return v

#==========================================================================
def connected_components(graph):
    num_nodes  = graph.nrows
    cc_ids     = grb.Vector.sparse(grb.types.UINT64, num_nodes)
    curr_cc_id = 0

    for src_node in range(num_nodes):
        if cc_ids.get(src_node) == None:
            # traverse from src_node marking all reachable nodes
            visited = bfs(graph, src_node)

            #cc_ids[visited] = curr_cc_id
            cc_ids.assign_scalar(curr_cc_id, mask=visited)
            curr_cc_id += 1

    return curr_cc_id, cc_ids

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
