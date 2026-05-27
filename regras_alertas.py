REGRAS_ALERTAS = {
    "uptime < 10m": {
        "descricao": "Totem reiniciado",
        "causa": "Possível reinicialização do equipamento"
    },

    "nvme0n1": {
        "descricao": "Lentidão ou falha no SSD",
        "causa": "Tempo de resposta alto no dispositivo de armazenamento"
    },

    "active checks": {
        "descricao": "Sem comunicação com o servidor Zabbix",
        "causa": "Host sem comunicação com o monitoramento"
    },

    "pinpad": {
        "descricao": "Falha de comunicação com pinpad",
        "causa": "Possível desconexão USB ou falha física"
    }
}