#
# https://blender.stackexchange.com/questions/45311/how-do-i-subdivide-f-curves/57453#57453
#

def correct_bezpart(p):
    if p[1].x <= p[2].x:
        return p

    scale = (p[3].x - p[0].x) / ( (p[1].x - p[0].x) + (p[3].x - p[2].x) )

    p = list(p)

    p[1] = p[0] + scale * (p[1]-p[0])
    p[2] = p[3] + scale * (p[2]-p[3])

    return p


def interp(v0, t, v1):
    return (1-t)*v0 + t*v1

def de_casteljeu(p ,t):
    q = [0,0,0,0]
    r = [0,0,0,0]

    q[0] = p[0]
    r[3] = p[3]

    q[1] = interp(p[0], t, p[1])
    x    = interp(p[1], t, p[2])
    r[2] = interp(p[2], t, p[3])

    #print([ r[2], '= interp(', p[2], t, p[3], ")" ])

    q[2] = interp(q[1], t, x)
    r[1] = interp(x, t, r[2])

    q[3] = r[0] = interp(q[2], t, r[1])

    return (q,r)



def subdivide_fcurve(fcurve, frame):

    orig_keyframe_count = len(fcurve.keyframe_points)

    fcurve.keyframe_points.add(1) # do this before we have any keyframe_points[i] references that would be invalidated
    kp9 = fcurve.keyframe_points[orig_keyframe_count]

    for i in range(1, orig_keyframe_count):
        kp0 = fcurve.keyframe_points[i-1]
        kp1 = fcurve.keyframe_points[i]
        if (kp1.co.x >=frame):
            break

    p = (kp0.co, kp0.handle_right, kp1.handle_left, kp1.co)
    p = correct_bezpart(p)

    t = tForFrame(frame, p[0].x, p[1].x, p[2].x, p[3].x)

    q,r = de_casteljeu(p,t)

    kp0.handle_right_type='ALIGNED'
    kp9.handle_left_type='ALIGNED'
    kp9.handle_right_type='ALIGNED'
    kp1.handle_left_type='ALIGNED'

    kp0.handle_right = q[1]
    kp9.handle_left = q[2]
    kp9.co = q[3]
    kp9.handle_right = r[1]
    kp1.handle_left = r[2]

    fcurve.update()


def bez_root_score(t):
    return max(abs(t.imag), 0-t.real, t.real-1)


def favorite_root(roots):
    """ Since we are confident that at least one of the roots is real, pick the one that has the imaginary component closest to zero
    """
    fav = roots[0]
    score = bez_root_score(fav)

    for i in range(1, len(roots)):
        if bez_root_score(roots[i]) < score:
            fav = roots[i]
            score = bez_root_score(roots[i])
    return fav


def tForFrame(fr, p0, p1, p2, p3):
    """
    fr = (1-t)**3 *p0 + 3*(1-t)**2 *t *p1 + 3*(1-t)* t**2 * p2 + t**3 *p3
    """

    import numpy

    coefficients = [
        -p0+3*p1-3*p2+p3,
        3*p0-6*p1+3*p2,
        -3*p0+3*p1,
        p0-fr
    ]

    roots = numpy.roots(coefficients)
    #print(roots)

    rval = favorite_root(roots).real

    sanity = bez(rval, p0,p1,p2,p3)
    if abs(sanity-fr) >1e-6:
        print(["defective", sanity, fr])
        print(roots)
        print([rval, "for", fr, p0, p1,p2,p3])

    if rval<0 or rval>1:
        print(["wiggy, bez(",rval,p0, p1,p2,p3,") = ",fr])
        print(roots)
        print([rval, "for", fr, p0, p1,p2,p3])
    return rval


def bez(t, p0, p1, p2, p3):
    s = 1-t

    return s*s*s*p0 + 3*s*s*t*p1 + 3*s*t*t*p2 + t*t*t*p3
