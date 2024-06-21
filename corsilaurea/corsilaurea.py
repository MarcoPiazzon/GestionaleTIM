from corsilaurea import *

from flask import abort


@corsilaurea_bp.route('/')
def corsilaureall():
    query_allcourselaurea=conn.execute(select(corsilaurea)).fetchall()
    return render_template("/corsilaurea/corsilaurea.html",courselaurea=query_allcourselaurea)

@corsilaurea_bp.route('/corsolaurea/<int:id>')
def singolocorsolaurea(id):
    corsiincorsi = conn.execute(select(join(corsilaurea,corsi)).where(corsi.c.codcorsolaurea == id)).fetchall()
    corsol = conn.execute(select(corsilaurea).where(corsilaurea.c.idcorsolaurea==id)).fetchone()
    if(not corsiincorsi):
        abort(404)
    return render_template("/corsilaurea/corsolaurea.html", c = corsiincorsi,corsl=corsol)
