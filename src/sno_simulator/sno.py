class SnøLag:
    def __init__(self, K_s: float, K_i: float) -> None:
        self.K_s = K_s
        self.K_i = K_i
        self.lag = [Sno(K_s)]

    @property
    def topp_lag(self):
        if len(self.lag) == 0:
            self.lag.append(Sno(self.K_s))
        return self.lag[-1]

    @property
    def dybde(self):
        return sum([lag.dybde for lag in self.lag])

    def smelting(self, temp) -> float:
        vann_i_systemet = 0
        vann_i_snøen = self.topp_lag.smelting(temp)
        if self.topp_lag.dybde == 0:
            self.lag.pop()
        if len(self.lag) < 2:
            vann_i_systemet = vann_i_snøen
        else:
            self.lag[-2].absorbering(vann_i_snøen)

        return vann_i_systemet

    def snøfall(self, snofall):
        if isinstance(self.topp_lag, Is):
            self.lag.append(Sno(self.K_s))
        self.topp_lag.snøfall(snofall)

    def minus(self):
        if self.topp_lag.fuktighet > 0:
            self.lag.append(Is(self.K_i, self.topp_lag.fuktighet))


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

    def absorbering(self, vann):
        self._fuktighet = self._fuktighet + vann

    def smelting(self, temp) -> float:
        smeltet_vann = 0
        self._fuktighet = self._snøsmelte_rate(temp) * self._dybde
        self._dybde = self._dybde - self._fuktighet
        if self._fuktighet > self._dybde * 0.6:
            smeltet_vann = self._fuktighet
            self._fuktighet = 0
        return smeltet_vann

    def snøfall(self, nedbør):
        self._dybde = self._dybde + nedbør

    @property
    def dybde(self):
        return self._dybde

    @property
    def fuktighet(self):
        return self._fuktighet

    @fuktighet.setter
    def fuktighet(self, value: float):
        self._fuktighet = value


class Is:
    def __init__(self, K_i: float, dybde: float = 0) -> None:
        self.K_i = K_i
        self.dybde = dybde

    def _is_smelte_rate(self, temp):
        rate = self.K_i * temp
        if rate > 1:
            return 1
        return rate

    def absorbering(self, vann):
        self.dybde = self.dybde + vann

    def smelting(self, temp) -> float:
        vann = self._is_smelte_rate(temp) * self.dybde
        self.dybde = self.dybde - vann
        return vann

    def dannelse(self, smeltet_sno):
        self.dybde = self.dybde + smeltet_sno

    @property
    def fuktighet(self):
        return 0
