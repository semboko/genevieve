def orientation(p, q, r):
    # returns 1 if cw
    # returns -1 if ccw
    # returns 0 otherwise
    Px, Py = p
    Qx, Qy = q
    Rx, Ry = r
    
    dx1 = Qx - Px
    dx2 = Rx - Qx
    dy1 = Qy - Py
    dy2 = Ry - Qy
    
    ds = dy1 * dx2 - dy2 * dx1
    
    if ds < 0:
        return -1
    
    if ds > 0:
        return 1
    
    return 0

def intersect(p1, p2, w1, w2):
    return (
        orientation(p1, p2, w1) != orientation(p1, p2, w2)
        and
        orientation(w1, w2, p1) != orientation(w1, w2, p2)
    )