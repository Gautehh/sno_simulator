class SnøLag:
    def __init__(self, K_s: float, K_i: float) -> None:
        self.K_s = K_s
        self.K_i = K_i
        self.lag: list[Is | Sno] = []
    
    @property
    def ingen_sno(self):
        return self.antall_snø_lag() == 0

    @property
    def øverste_lag(self):
        return self.lag[-1]
    
    @property
    def antall_snø_lag(self):
        return len(self.lag)

    @property
    def dybde(self):
        return sum([lag.dybde for lag in self.lag])
    
    def fjerne_øverste_lag_dersom_smeltet(self):
        if self.øverste_lag.dybde == 0:
            self.lag.pop()

    def absorbering_av_vann_fra_øvrige_lag(self, vann_i_snøen) -> float:
        """Absorberer av vann i underliggende snø, dersom det er et lag med snø
        så går vannet ut i systemet """
        if self.antall_snø_lag == 1:
            return vann_i_snøen
        else:
            self.lag[-2].absorbering(vann_i_snøen)
            return 0
            
    
    def smelting(self, temp) -> float:
        if self.ingen_sno():
            return 0
        vann_i_snøen = self.øverste_lag.smelting(temp)
        self.fjerne_øverste_lag_dersom_smeltet()
        vann_i_systemet = self.absorbering_av_vann_fra_øvrige_lag(vann_i_snøen)

        return vann_i_systemet

    def snøfall(self, snofall: float):
        if self.ingen_sno() or isinstance(self.øverste_lag, Is):
            self.lag.append(Sno(self.K_s))
        self.øverste_lag.snøfall(snofall)

    def minus(self):
        if self.ingen_sno:
            return
        if self.øverste_lag.fuktighet > 0:
            self.lag.append(Is(self.K_i, self.øverste_lag.fuktighet))

class Sno:
    def __init__(self, K_s: float) -> None:
        self.K_s = K_s
        self._dybde = 0
        self._fuktighet = 0

    def _snøsmelte_rate(self, temp):
        rate = self.K_s * temp
        if rate > 1:
            return 1
        return rate

    def absorbering(self, vann: float):
        """Absorberer vann i snøen"""

        self._fuktighet = self._fuktighet + vann

    def smelting(self, temp) -> float:
        """Smelter snøen og returnerer smeltet vann
        gitt at funktighet er større enn 60% av dybde"""
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
        return self._dybde

    @property
    def fuktighet(self):
        return self._fuktighet


class Is:
    def __init__(self, K_i: float, dybde: float = 0) -> None:
        self.K_i = K_i
        self._dybde = dybde

    def _is_smelte_rate(self, temp):
        rate = self.K_i * temp
        if rate > 1:
            return 1
        return rate

    def smelting(self, temp) -> float:
        """Smelting av is og returnerer smeltet vann"""
        vann = self._is_smelte_rate(temp) * self._dybde
        self._dybde = self._dybde - vann
        return vann

    def dannelse(self, smeltevann):
        """Dannelse av is ved at smeltetvann fryser til is"""
        self._dybde = self._dybde + smeltevann
    
    def absorbering(self, vann: float):
        """Absorberer vann i isen"""
        self.dannelse(vann)

    @property
    def dybde(self):
        return self._dybde
