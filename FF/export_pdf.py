from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from FF.models import LapData, Penaty, CarStatus, SessionData, TypeStint, SessionModel
    
def export_all_data_to_pdf(filepath):
        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter
        y = height - 40
        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, y, "Relatório Completo F1")
        y -= 30
    
        # LapData
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y, "Voltas (LapData):")
        y -= 20
        c.setFont("Helvetica", 10)
        for lap in LapData.objects.all().order_by('volta', 'carro_id'):
            line = (
                f"Volta {lap.volta} | Carro {lap.carro_id} | Piloto {lap.nome_piloto} | "
                f"Tempo: {lap.tempo_volta}s | Setores: {lap.tempo_setor1}/{lap.tempo_setor2}/{lap.tempo_setor3} | "
                f"Posição: {lap.posicao} | Válida: {lap.volta_valida}"
            )
            c.drawString(40, y, line)
            y -= 15
            if y < 40:
                c.showPage()
                y = height - 40
    
        # Penaty
        y -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y, "Penalidades (Penaty):")
        y -= 20
        c.setFont("Helvetica", 10)
        for pen in Penaty.objects.all().order_by('volta', 'carro_id'):
            line = (
                f"Volta {pen.volta} | Carro {pen.carro_id} | Piloto {pen.nome_piloto} | "
                f"Tipo: {pen.tipo_punicao} | Tempo: {pen.tempo_punicao}s | Cumprida: {pen.cumprida}"
            )
            c.drawString(40, y, line)
            y -= 15
            if y < 40:
                c.showPage()
                y = height - 40
    
        # CarStatus
        y -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y, "Status do Carro (CarStatus):")
        y -= 20
        c.setFont("Helvetica", 10)
        for status in CarStatus.objects.all().order_by('timestamp'):
            line = (
                f"Piloto: {status.nome_piloto} | Carro: {status.carro_id} | Pneus: {status.tipo_pneus} | "
                f"Desgaste: {status.desgaste_pneus} | Dano Frontal: {status.dano_aerodinamicos_frontal}%"
            )
            c.drawString(40, y, line)
            y -= 15
            if y < 40:
                c.showPage()
                y = height - 40
    
        # SessionData
        y -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y, "Sessões (SessionData):")
        y -= 20
        c.setFont("Helvetica", 10)
        for sess in SessionData.objects.all().order_by('timestamp'):
            line = (
                f"Pista: {sess.pista} | Clima: {sess.clima} | Temp. Pista: {sess.temperatura_pista}°C | "
                f"Temp. Ar: {sess.temperatura_ar}°C | Voltas: {sess.num_voltas}"
            )
            c.drawString(40, y, line)
            y -= 15
            if y < 40:
                c.showPage()
                y = height - 40
    
        # TypeStint
        y -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y, "Stints de Pneus (TypeStint):")
        y -= 20
        c.setFont("Helvetica", 10)
        for stint in TypeStint.objects.all().order_by('carro_id', 'stint_num'):
            line = (
                f"Piloto: {stint.nome_piloto} | Carro: {stint.carro_id} | Stint: {stint.stint_num} | "
                f"Pneu: {stint.tipo_pneu_real}/{stint.tipo_pneu_visual} | Voltas: {stint.volta_inicio}-{stint.volta_fim}"
            )
            c.drawString(40, y, line)
            y -= 15
            if y < 40:
                c.showPage()
                y = height - 40
    
        # SessionModel
        y -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y, "Sessões Completas (SessionModel):")
        y -= 20
        c.setFont("Helvetica", 10)
        for sm in SessionModel.objects.all().order_by('timestamp'):
            line = (
                f"Pista: {sm.track} | Temp. Pista: {sm.trackTemperature}°C | Temp. Ar: {sm.airTemperature}°C | "
                f"Voltas: {sm.nbLaps} | Jogadores: {sm.nb_players} | Sessão: {sm.Seance}"
            )
            c.drawString(40, y, line)
            y -= 15
            if y < 40:
                c.showPage()
                y = height - 40
    
        c.save()
        print(f"PDF salvo em {filepath}")