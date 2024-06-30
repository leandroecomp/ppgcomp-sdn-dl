import numpy as np


class Flow:
    def __init__(self, nw_src, tp_src, nw_dst, tp_dst, nw_proto, request_time):

        # tupla de informações do fluxo
        self.nw_src = nw_src  # IP de origem
        self.tp_src = tp_src  # Porta de origem
        self.nw_dst = nw_dst  # IP de destino
        self.tp_dst = tp_dst  # Porta de destino
        self.nw_proto = nw_proto  # Código da camada de transporte
        self.request_time = request_time  # periodicidade de coleta

        # timestamp de criação do fluxo
        # self.OVS_start_flow = OVS_start_flow

        # contadores nativos Openflow
        self.OVS_duration_flow = 0  # Duração do fluxo
        self.OVS_packet_count = 0  # Contador de pacotes
        self.OVS_byte_count = 0  # Contador de bytes

        # Status
        # self.acative=True

        # contador de amostra corrente
        self.next_sample = 1

        # características primárias
        self.pc = 0
        self.bc = 0

        # características secundárias
        self.pl = []
        self.piat = []
        self.pps = 0
        self.bps = 0

        # características estatísticas
        self.pl_mean = 0
        self.piat_mean = 0
        self.pps_mean = 0
        self.bps_mean = 0

        self.pl_var = 0
        self.piat_var = 0
        self.pps_var = 0
        self.bps_var = 0

        self.pl_q1 = 0
        self.pl_q3 = 0
        self.piat_q1 = 0
        self.piat_q3 = 0

        # características escalares
        self.pl_max = 0
        self.pl_min = 0
        self.piat_max = 0
        self.piat_min = 0
        self.pps_max = 0
        self.pps_min = 0
        self.bps_max = 0
        self.bps_min = 0
        # self.duration     = 0;
        # self.size_packets = 0;
        # self.size_bytes   = 0;
        # self.category = self.get_protocol(portdict)

    def print(self):
        print(self.nw_src, self.tp_src, self.nw_dst, self.tp_dst, self.nw_proto)

    def update(self, OVS_duration_flow, OVS_packet_count, OVS_byte_count):
        # cria variáveis para a armazenar valores
        # anterioes de média e variância
        pps_mean_0 = self.pps_mean
        bps_mean_0 = self.bps_mean
        pps_var_0 = self.pps_var
        bps_var_0 = self.bps_var
        pl_min_0 = self.pl_min
        piat_min_0 = self.piat_min
        pps_max = self.pps_max
        pps_min_0 = self.pps_min
        bps_max = self.bps_max
        bps_min_0 = self.bps_min

        # self.duration = OVS_duration_flow
        # self.size_packets = OVS_packet_count
        # self.size_bytes   = OVS_byte_count

        # print(self.next_sample)
        if self.next_sample == 1:
            # print("primeiro snap")
            # a primeira amostra (snapshot) de um fluxo precisa de uma tratamento
            # estatístico. Já que por muitas vezes o ausência de novos pacotes pode acabar zerando
            # os campos. Para evitar isso ao invés de considerar a contabilização dos contadores pc e bc,
            # para a primeira amostra é utilizada uma aproximação calculada com request_time,
            # OVS_duration_flow, OVS_packet_count, OVS_byte_count.

            if OVS_duration_flow < self.request_time:
                delta_t = OVS_duration_flow
                self.pc = OVS_packet_count
                self.bc = OVS_byte_count
                self.piat.append(0 if self.pc == 0 else delta_t / OVS_packet_count)
                self.pps = (
                    0 if (self.pc == 0 or delta_t == 0) else OVS_packet_count / delta_t
                )
                self.bps = (
                    0 if (self.bc == 0 or delta_t == 0) else OVS_byte_count / delta_t
                )
            else:
                delta_t = self.request_time
                self.pc = delta_t * OVS_packet_count / OVS_duration_flow
                self.bc = delta_t * OVS_byte_count / OVS_duration_flow
                self.piat.append(0 if self.pc == 0 else delta_t / self.pc)
                self.pps = 0 if (self.pc == 0 or delta_t == 0) else self.pc / delta_t
                self.bps = 0 if (self.bc == 0 or delta_t == 0) else self.bc / delta_t

            self.pl.append(0 if self.pc == 0 else self.bc / self.pc)

            self.pl_mean = self.pl[0]
            self.piat_mean = self.piat[0]

            self.pps_mean = self.pps
            self.bps_mean = self.bps

            self.pl_var = 0
            self.piat_var = 0
            self.pps_var = 0
            self.bps_var = 0

            self.pl_q1 = self.pl[0]
            self.pl_q3 = self.pl[0]
            self.piat_q1 = self.piat[0]
            self.piat_q3 = self.piat[0]

            self.pl_max = self.pl[0]
            self.pl_min = self.pl[0]
            self.piat_max = self.piat[0]
            self.piat_min = self.piat[0]

            self.pps_max = self.pps
            self.pps_min = self.pps
            self.bps_max = self.bps
            self.bps_min = self.bps

            # self.duration = delta_t
            # self.size_packets = self.pc
            # self.size_bytes   = self.bc
        else:
            if (
                (self.OVS_duration_flow > OVS_duration_flow)
                or (self.OVS_packet_count > OVS_packet_count)
                or (self.OVS_byte_count > OVS_byte_count)
            ):
                if OVS_duration_flow < self.request_time:
                    # print("Code 10: duração menor que request ")
                    delta_t = OVS_duration_flow
                    self.pc = OVS_packet_count
                    self.bc = OVS_byte_count
                    self.piat.append(0 if self.pc == 0 else delta_t / OVS_packet_count)
                    self.pps = (
                        0
                        if (self.pc == 0 or delta_t == 0)
                        else OVS_packet_count / delta_t
                    )
                    self.bps = (
                        0
                        if (self.bc == 0 or delta_t == 0)
                        else OVS_byte_count / delta_t
                    )
                else:
                    # print("Code 20: duração maior que request ")
                    delta_t = self.request_time
                    self.pc = delta_t * OVS_packet_count / OVS_duration_flow
                    self.bc = delta_t * OVS_byte_count / OVS_duration_flow
                    self.piat.append(0 if self.pc == 0 else delta_t / self.pc)
                    self.pps = (
                        0 if (self.pc == 0 or delta_t == 0) else self.pc / delta_t
                    )
                    self.bps = (
                        0 if (self.bc == 0 or delta_t == 0) else self.bc / delta_t
                    )
            else:
                # print("Code 30: snapshot padrão ")

                delta_t = OVS_duration_flow - self.OVS_duration_flow
                self.pc = OVS_packet_count - self.OVS_packet_count
                self.bc = OVS_byte_count - self.OVS_byte_count
                self.piat.append(0 if self.pc == 0 else delta_t / self.pc)
                self.pps = 0 if (self.pc == 0 or delta_t == 0) else self.pc / delta_t
                self.bps = 0 if (self.bc == 0 or delta_t == 0) else self.bc / delta_t

            self.pl.append(0 if self.pc == 0 else self.bc / self.pc)

            self.pl_mean = ((self.next_sample - 1) * self.pl_mean + self.pl[-1]) / (
                self.next_sample
            )
            self.piat_mean = (
                (self.next_sample - 1) * self.piat_mean + self.piat[-1]
            ) / (self.next_sample)

            self.pps_mean = ((self.next_sample - 1) * self.pps_mean + self.pps) / (
                self.next_sample
            )
            self.bps_mean = ((self.next_sample - 1) * self.bps_mean + self.bps) / (
                self.next_sample
            )

            self.pl_var = np.var(self.pl, ddof=0)
            self.piat_var = np.var(self.piat, ddof=0)
            self.pps_var = ((self.next_sample - 1) / self.next_sample) * (
                pps_var_0 + pow(self.pps - pps_mean_0, 2) / self.next_sample
            )
            self.bps_var = ((self.next_sample - 1) / self.next_sample) * (
                bps_var_0 + pow(self.bps - bps_mean_0, 2) / self.next_sample
            )

            self.pl_q1 = np.quantile(self.pl, 0.25)
            self.pl_q3 = np.quantile(self.pl, 0.75)
            self.piat_q1 = np.quantile(self.piat, 0.25)
            self.piat_q3 = np.quantile(self.piat, 0.75)

            self.pl_max = max(self.pl)
            # self.pl_min = (self.pl[-1] if ( (self.pl[-1] < pl_min_0) and ( self.pl[-1] > 0 ) ) else pl_min_0)
            self.pl_min = (
                self.pl[-1]
                if (
                    ((self.pl[-1] < self.pl_min) and (self.pl[-1] > 0))
                    or (self.pl_min == 0)
                )
                else self.pl_min
            )

            self.piat_max = max(self.piat)
            # self.piat_min = (self.piat[-1] if ( (self.piat[-1] < piat_min_0) and ( self.piat[-1] > 0 ) ) else piat_min_0)
            self.piat_min = (
                self.piat[-1]
                if (
                    ((self.piat[-1] < self.piat_min) and (self.piat[-1] > 0))
                    or (self.piat_min == 0)
                )
                else self.piat_min
            )

            self.pps_max = self.pps if self.pps > pps_max else pps_max
            # self.pps_min = (self.pps if ( (self.pps < pps_min_0) and ( self.pps > 0 ) ) else pps_min_0)
            self.pps_min = (
                self.pps
                if (
                    ((self.pps < self.pps_min) and (self.pps > 0))
                    or (self.pps_min == 0)
                )
                else self.pps_min
            )

            self.bps_max = self.bps if self.bps > bps_max else bps_max
            # self.bps_min = (self.bps if ( (self.bps < bps_min_0) and ( self.bps > 0 ) ) else bps_min_0)
            self.bps_min = (
                self.bps
                if (
                    ((self.bps < self.bps_min) and (self.bps > 0))
                    or (self.bps_min == 0)
                )
                else self.bps_min
            )

        self.OVS_duration_flow = OVS_duration_flow
        self.OVS_packet_count = OVS_packet_count
        self.OVS_byte_count = OVS_byte_count
        self.next_sample += 1
