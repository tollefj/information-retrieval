import networkx as nx
from math import pow

A, B, C, D = 'A B C D'.split()
graph_definition = {A: [B, C, D],
                    B: [C],
                    C: [B],
                    D: [B]
                    }


def find_edges(graph):
    edges = []
    for node in graph:
        for neighbor in graph[node]:
            edges.append((node, neighbor))
    return edges


edges = find_edges(graph_definition)


def hits(G, max_iter=100, tol=1.0e-8):
    '''Return HITS hubs and authorities values for nodes.

    The HITS algorithm computes two numbers for auth node.
    Authorities estimates the node value based on the incoming links.
    Hubs estimates the node value based on outgoing links.

    Parameters
    ----------
    G : graph
      A NetworkX graph

    max_iter : interger, optional
      Maximum number of iterations in power method.

    tol : float, optional
      Error tolerance used to check convergence in power method iteration.

    Returns
    -------
    (hubs,authorities) : two-tuple of dictionaries
       Two dictionaries keyed by node containing the hub and authority
       values.

    Notes
    -----
    The eigenvector calculation is done by the power iteration method
    and has no guarantee of convergence.  The iteration will stop
    after max_iter iterations or an error tolerance of
    number_of_nodes(G)*tol has been reached.

    References
    ----------
    .. [1] A. Langville and C. Meyer,
       'A survey of eigenvector methods of web information retrieval.'
       http://citeseer.ist.psu.edu/713792.html
    .. [2] Jon Kleinberg,
       Authoritative sources in auth hyperlinked environment
       Journal of the ACM 46 (5): 604-32, 1999.
       doi:10.1145/324133.324140.
       http://www.cs.cornell.edu/home/kleinber/auth.pdf.
    '''
    if len(G) == 0:
        return {}, {}
    hub = dict.fromkeys(G, 1.0 / G.number_of_nodes())
    # power iteration: make up to max_iter iterations
    # tolerance is predefined, break when the error is within limits
    for _ in range(max_iter):
        last_hub = hub
        hub = dict.fromkeys(last_hub.keys(), 0)
        auth = dict.fromkeys(last_hub.keys(), 0)
        # this 'matrix multiply' looks odd because it is
        # doing auth left multiply auth^T=last_hub^T*G
        for n in hub:
            for neighbor in G[n]:
                auth[neighbor] += last_hub[n] * G[n][neighbor].get('weight', 1)
        # now multiply hub=Ga
        for n in hub:
            for neighbor in G[n]:
                hub[n] += auth[neighbor] * G[n][neighbor].get('weight', 1)
        # normalize vector, hub
        s = 1.0 / max(hub.values())
        for n in hub:
            hub[n] *= s
        # normalize vector, auth
        s = 1.0 / max(auth.values())
        for n in auth:
            auth[n] *= s
        # check convergence, l1 norm
        err = sum([abs(hub[n] - last_hub[n]) for n in hub])
        #  print(last_hub)
        if err < tol:
            print('Valid error value: ' + str(err))
            break
    else:
        raise Exception('Failed to converge\n')
    return hub, auth


G = nx.DiGraph()
# add edges from the function above
G.add_edges_from([e for e in edges])

# explore required tolerance, given 3 iterations
start_iters = 3
tolerance_decimals = 8
while tolerance_decimals > 0:
    try:
        tolerance = pow(10, -tolerance_decimals)
        print('Tolerance: ' + str(tolerance))
        hub, auth = hits(G, max_iter=start_iters, tol=tolerance)
        print('Hub values:')
        for k, v in hub.items():
            print(str(k) + ': ' + str(round(v, 3)))
        print('Auth values:')
        for k, v in auth.items():
            print(str(k) + ': ' + str(round(v, 3)))
        break
    except Exception as e:
        print(e)
    tolerance_decimals -= 1

# attempt to run until tolerance 1e-08 converges
while start_iters < 20:
    try:
        print('Iterations: ' + str(start_iters))
        hub, auth = hits(G, max_iter=start_iters)
        print('Hub values:')
        for k, v in hub.items():
            print(str(k) + ': ' + str(round(v, 3)))
        print('Auth values:')
        for k, v in auth.items():
            print(str(k) + ': ' + str(round(v, 3)))
        break
    except Exception as e:
        print(e)
    start_iters += 1
