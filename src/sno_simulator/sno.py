class Sno:
    def __init__(self, K_s: float) -> None:
        self.K_s = K_s
        self._dybde = 0
        self._fuktighet = 0

    def _snøsmelte_rate(self, temperatur: float):
        """Beregner smelte rate til snøen, raten er mellom 0 og 1"""
        rate = self.K_s * temperatur
        if rate > 1:
            return 1
        return rate

    def absorbering(self, vann: float):
        """Absorbering av vann i snøen"""

        self._fuktighet = self._fuktighet + vann

    def smelting(self, temp) -> float:
        """Smelter snøen og returnerer smeltet vann
        gitt at mengden funktighet er større enn 60% av mengden snø"""
        smeltet_vann = 0
        self._fuktighet = self._snøsmelte_rate(temp) * self._dybde
        self._dybde = self._dybde - self._fuktighet
        if self._fuktighet > self._dybde * 0.6:
            smeltet_vann = self._fuktighet
            self._fuktighet = 0
        return smeltet_vann

    def snøfall(self, nedbør: float):
        """Økning av snydybde ved snøfall"""
        self._dybde = self._dybde + nedbør

    @property
    def dybde(self):
        """Returnerer dybden av snøen"""
        return self._dybde

    @property
    def mengden_fuktighet(self):
        """Returnerer mengden fuktigheten i snøen"""
        return self._fuktighet


class Is:
    def __init__(self, K_i: float, dybde: float = 0) -> None:
        self.K_i = K_i
        self._dybde = dybde

    def _is_smelte_rate(self, temperatur: float):
        """Beregner smelte rate til isen, raten er mellom 0 og 1"""
        rate = self.K_i * temperatur
        if rate > 1:
            return 1
        return rate

    def smelting(self, temperatur: float) -> float:
        """Smelting av is og returnerer smeltet vann"""
        vann = self._is_smelte_rate(temperatur) * self._dybde
        self._dybde = self._dybde - vann
        return vann

    def dannelse(self, smeltevann: float):
        """Dannelse av is ved at smeltetvann fryser til is"""
        self._dybde = self._dybde + smeltevann

    def absorbering(self, vann: float):
        """Absorberer vann i isen blir modelert som at vannet fryser til is i kontakt med isen"""
        self.dannelse(vann)

    @property
    def dybde(self) -> float:
        """Returnerer dybden av isen"""
        return self._dybde

    @property
    def mengden_fuktighet(self):
        """Mengden fuktighet i isen er modellert som 0"""
        return 0


class SnøLag:
    def __init__(self, K_s: float, K_i: float) -> None:
        self.K_s = K_s
        self.K_i = K_i
        self.lag: list[Is | Sno] = []

    @property
    def bart(self) -> bool:
        """Returnerer True dersom det er bart"""
        return self.antall_snø_lag == 0

    @property
    def øverste_lag(self) -> Is | Sno:
        """Returnerer øverste lag"""
        return self.lag[-1]

    @property
    def antall_snø_lag(self) -> int:
        """Returnerer antall snølag"""
        return len(self.lag)

    @property
    def dybde(self):
        """Returnerer dybden av snølagene"""
        return sum([lag.dybde for lag in self.lag])

    def fjerner_øverste_lag_dersom_smeltet(self):
        """Fjerner øverste lag dersom det er smeltet helt
        """
        if self.øverste_lag.dybde == 0:
            self.lag.pop()

    def absorbering_av_vann_fra_øvrige_lag(self, vann_i_snøen: float) -> float:
        """Absorberer av vann i underliggende snø, dersom det er et lag med snø
        så går vannet ut i systemet"""
        if self.antall_snø_lag == 1:
            return vann_i_snøen
        else:
            self.lag[-2].absorbering(vann_i_snøen)
            return 0

    def smelting(self, temepratur: float) -> float:
        """Beregner smelting av snøen og returnerer eventulet vann ute av systemet

        :param temepratur: temperatur i lufta
        :type temp: float
        :return: vann som renner ut av systemet
        :rtype: float
        """
        if self.bart:
            return 0
        vann_i_snøen = self.øverste_lag.smelting(temepratur)
        vann_ute_av_systemet = self.absorbering_av_vann_fra_øvrige_lag(vann_i_snøen)
        self.fjerner_øverste_lag_dersom_smeltet()

        return vann_ute_av_systemet

    def snøfall(self, snofall: float):
        """Legger til snø i det øverste laget
        """
        if self.bart or isinstance(self.øverste_lag, Is):
            self.lag.append(Sno(self.K_s))
        self.øverste_lag.snøfall(snofall)

    def is_dannelse(self):
        """Danner et skare lag dersom det er fuktig snø i det øverste laget
        """
        if self.bart:
            return
        if self.øverste_lag.mengden_fuktighet > 0:
            self.lag.append(Is(self.K_i, self.øverste_lag.mengden_fuktighet))
