#
# Developed by 10Pines SRL
# License: 
# This work is licensed under the 
# Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. 
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ 
# or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, 
# California, 94041, USA.
#  
import unittest

class Numero:
    DESCRIPCION_DE_ERROR_DE_DIVISION_POR_CERO = 'No se puede dividir por 0'

    def esCero(self):
        self.shouldBeImplementedBySubclass()

    def esUno(self):
        self.shouldBeImplementedBySubclass()

    def __add__(self,sumando):
        self.shouldBeImplementedBySubclass()

    def __mul__(self,factor):
        self.shouldBeImplementedBySubclass()
    
    def __div__(self,divisor):
        self.shouldBeImplementedBySubclass()

    def shouldBeImplementedBySubclass(self):
        raise NotImplementedError('Should be implemented by the subclass')

class Entero(Numero):
    
    def __init__(self, numero):
        self._valor = numero

    def valor(self):
        return self._valor
    
    def esCero(self):
        return self._valor == 0

    def esUno(self):
        return self._valor == 1

    def __eq__(self,anObject):
        return self.mismaClaseYmismoValor(anObject)
    
    def mismaClaseYmismoValor(self,anObject):
        return isinstance(anObject, self.__class__) and self._valor==anObject._valor
    
    def __add__(self,sumando):
        
        return sumando.sumarEntero(self)
        
        # if isinstance(sumando, self.__class__):
        #     return Entero(self._valor+sumando.valor())
        # elif isinstance(sumando, Fraccion):
        #     return Entero((self._valor*sumando.denominador().valor() + sumando.numerador().valor())) /  sumando.denominador()
 
    def __mul__(self,factor):
        return factor.multiplicarEntero(self)
        '''
        if isinstance(factor, self.__class__):
            return Entero(self._valor*factor.valor())
        elif isinstance(factor, Fraccion):
            return Entero(self._valor * factor.numerador().valor()) / factor.denominador()
        '''
    def __div__(self,divisor):
        return divisor.dividirEntero(self)
        '''
        if isinstance(divisor, self.__class__):
            return divisor.dividirEntero(self)
        elif isinstance(divisor, Fraccion):
            return self * divisor.denominador() / divisor.numerador()
        '''
    def sumarEntero(self,sumando):
        return Entero(self._valor + sumando.valor())

    def sumarFraccion(self,sumando):
        return Entero((self._valor*sumando.denominador().valor() + sumando.numerador().valor())) /  sumando.denominador()
    
    def multiplicarEntero(self,factor):
        return Entero(self._valor*factor.valor())
        
    def multiplicarFraccion(self,factor):
        return Entero(self._valor * factor.numerador().valor()) / factor.denominador()
        
    def dividirFraccion(self,dividendo):
        return dividendo * (Entero(1) / self)
    
    def dividirEntero(self,dividendo):
        if self.esCero():  ##De alguna forma hay que hacer que el objeto 0 sepa responder dividirEntero pero que su respuesta 
                           ##sea levantar la excepcion, y que la de todos los demas numeros hacer esto, 
                           ##lo unico que se me ocurre es por aca "should be implemented by subclass", crear en la jerarquia abajo de entero dos clases, una 
                           ##EnterosDistintosDe0 Y otra CeroClass ... horrible pero bueno. Creo que no hay muchas opciones.
            raise Exception(Numero.DESCRIPCION_DE_ERROR_DE_DIVISION_POR_CERO)
        if self.esUno():
            return dividendo
        
        maximoComunDivisor = self.maximoComunDivisorCon(dividendo)
        #No puedo usar / porque puedo caer en una recursion, por eso divido directamente
        #los valores porque se que son enteros
        numerador = dividendo.divisionEntera(maximoComunDivisor)
        denominador = self.divisionEntera(maximoComunDivisor)
        
        if denominador.esUno():
            return numerador
        
        return Fraccion(numerador,denominador)

    def divisionEntera(self,divisorEntero):
        return Entero (self._valor / divisorEntero.valor())
            
    def maximoComunDivisorCon(self,otroEntero):
        if otroEntero.esCero(): 
            return self
        else:
            return otroEntero.maximoComunDivisorCon(self.restoCon(otroEntero))
    
    def restoCon(self, divisor):
        return Entero (self._valor % divisor.valor());
        
    
class Fraccion(Numero):
    
    def __init__(self, numerador, denominador): ##Para mi hay que reducir aca y mantener el invariante, los tests 15 y 16 pasan desde un principio pero porque los create crean con a/b. 
        self._numerador = numerador
        self._denominador = denominador

    def numerador(self):
        return self._numerador
    
    def denominador(self):
        return self._denominador
    
    def esCero(self):
        return False

    def esUno(self):
        return False

    def __eq__(self,anObject):
        return self.mismaClaseYmismoValor(anObject)
    
    def mismaClaseYmismoValor(self,anObject):
        return isinstance(anObject, self.__class__) and (self._numerador*anObject.denominador()==self._denominador*anObject.numerador() )
    
    def __add__(self,sumando):  #sumando puede ser entero
        
        # if isinstance(sumando, self.__class__):
        #     nuevoDenominador = self._denominador * sumando.denominador()
        #     primerSumando = self._numerador * sumando.denominador()
        #     segundoSumando = self._denominador * sumando.numerador()
        #     nuevoNumerador = primerSumando + segundoSumando
        #     return nuevoNumerador / nuevoDenominador
        # elif isinstance(sumando, Entero):
        #     return Entero((sumando.valor()*self.denominador().valor() + self.numerador().valor())) /  self.denominador()

        return sumando.sumarFraccion(self)    
            
        
    def __mul__(self,factor):
        return factor.multiplicarFraccion(self)
        '''
        if isinstance(factor, self.__class__):
            return (self._numerador * factor.numerador()) / (self._denominador * factor.denominador())
        elif isinstance(factor, Entero):
             return factor * self
        #No estoy seguro de si eso se puede hacer... (?)
        #Para mi no pongamos eso porque nos van a decir que dependemos del otro, mas facil por las dudas directamente hacer
        # return Entero(self.numerador().valor() * factor.valor()) / self.denominador()
        '''
    def __div__(self,divisor):
        return divisor.dividirFraccion(self)
        '''
        if isinstance(divisor, self.__class__):
            return divisor.dividirFraccion(self)
        elif isinstance(divisor, Entero):
            return self * (Entero(1) / divisor)
            # o return self.numerador()/ Entero(self.denominador().valor()*divisor.valor()) para no depender de la multiplicacion de Enteros
        #Recycling
        '''

    def sumarEntero(self,sumando):
        return Entero((sumando.valor()*self.denominador().valor() + self.numerador().valor())) /  self.denominador()    
     
    def sumarFraccion(self,sumando):
        nuevoDenominador = self._denominador * sumando.denominador()
        primerSumando = self._numerador * sumando.denominador()
        segundoSumando = self._denominador * sumando.numerador()
        nuevoNumerador = primerSumando + segundoSumando
        return nuevoNumerador / nuevoDenominador
    
    def multiplicarEntero(self,factor):
        return Entero(self.numerador().valor() * factor.valor()) / self.denominador()
        
    def multiplicarFraccion(self,factor):
        return (self._numerador * factor.numerador()) / (self._denominador * factor.denominador())
        
    def dividirEntero(self,dividendoEntero):
        return dividendoEntero * (self.denominador() / self.numerador()) 
        
    def dividirFraccion(self,dividendo):
        return (dividendo.numerador() * self._denominador) / (dividendo.denominador () * self._numerador)

class NumeroTest(unittest.TestCase):

    def createCero(self):
        return Entero(0)
    
    def createUno(self):
        return Entero(1)
    
    def createDos(self):
        return Entero(2)
    
    def createTres(self):
        return Entero(3)
    
    def createCuatro(self):
        return Entero(4)
    
    def createCinco(self):
        return Entero(5)
    
    def createUnQuinto(self):
        return self.uno / self.cinco
    
    def createDosQuintos(self):
        return self.dos / self.cinco
    
    def createTresQuintos(self):
        return self.tres / self.cinco
    
    def createDosVeinticincoavos(self):
        return self.dos / Entero(25)
    
    def createUnMedio(self):
        return self.uno / self.dos
    
    def createCincoMedios(self):
        return self.cinco / self.dos
    
    def createSeisQuintos(self):
        return Entero(6) / self.cinco
    
    def createCuatroMedios(self):
        return self.cuatro / self.dos
    
    def createDosCuartos(self):
        return self.dos / self.cuatro

    def setUp(self):
        self.cero = self.createCero()
        self.uno = self.createUno()
        self.dos = self.createDos()
        self.tres = self.createTres()
        self.cuatro = self.createCuatro()
        self.cinco = self.createCinco()
        self.unQuinto = self.createUnQuinto()
        self.dosQuintos = self.createDosQuintos()
        self.tresQuintos = self.createTresQuintos()
        self.dosVeinticincoavos = self.createDosVeinticincoavos()
        self.unMedio = self.createUnMedio()
        self.cincoMedios = self.createCincoMedios()
        self.seisQuintos = self.createSeisQuintos()
        self.cuatroMedios = self.createCuatroMedios()
        self.dosCuartos = self.createDosCuartos()
             
    def test01EsCeroDevuelveTrueSoloParaElCero(self):
        self.assertTrue (self.cero.esCero())
        self.assertFalse (self.uno.esCero())

    def test02EsUnoDevuelveTrueSoloParaElUno(self):
        self.assertTrue (self.uno.esUno())
        self.assertFalse (self.cero.esUno())

    def test03SumaDeEnteros(self):
        self.assertEqual (self.dos,self.uno+self.uno)
    
    def test04MultiplicacionDeEnteros(self):
        self.assertEqual(self.cuatro, self.dos*self.dos)

    def test05DivisionDeEnteros(self):
        self.assertEqual(self.uno, self.dos/self.dos)
    
    def test06SumaDeFracciones(self):
        sieteDecimos = Entero(7) / Entero (10) # <- REEMPLAZAR POR LO QUE CORRESPONDA;   preguntar
        self.assertEqual (sieteDecimos,self.unQuinto+self.unMedio)
        # 
        # La suma de fracciones es:
        # 
        # a/b + c/d = (a.d + c.b) / (b.d)
        # 
        # SI ESTAN PENSANDO EN LA REDUCCION DE FRACCIONES NO SE PREOCUPEN!
        # NO SE ESTA TESTEANDO ESE CASO
        #

    def test07MultiplicacionDeFracciones(self):
        self.assertEqual (self.dosVeinticincoavos,self.unQuinto*self.dosQuintos)
        # 
        # La multiplicacion de fracciones es:
        # 
        # (a/b) * (c/d) = (a.c) / (b.d)
        # 
        # SI ESTAN PENSANDO EN LA REDUCCION DE FRACCIONES NO SE PREOCUPEN!
        # TODAVIA NO SE ESTA TESTEANDO ESE CASO
        #
    
    def test08DivisionDeFracciones(self):
        self.assertEqual (self.cincoMedios,self.unMedio/self.unQuinto)
        # 
        # La division de fracciones es:
        # 
        # (a/b) / (c/d) = (a.d) / (b.c)
        # 
        # SI ESTAN PENSANDO EN LA REDUCCION DE FRACCIONES NO SE PREOCUPEN!
        # TODAVIA NO SE ESTA TESTEANDO ESE CASO
        #

    # 
    # Ahora empieza lo lindo! - Primero hacemos que se puedan sumar enteros con fracciones
    # y fracciones con enteros 
    #
    def test09SumaDeEnteroYFraccion(self):
        self.assertEqual (self.seisQuintos,self.uno+self.unQuinto)
    
    def test10SumaDeFraccionYEntero(self):
        self.assertEqual (self.seisQuintos,self.unQuinto+self.uno)

    # 
    # Hacemos lo mismo para la multipliacion
    #
    def test11MultiplicacionDeEnteroPorFraccion(self):
        self.assertEqual(self.dosQuintos,self.dos*self.unQuinto)
    
    def test12MultiplicacionDeFraccionPorEntero(self):
        self.assertEqual(self.dosQuintos,self.unQuinto*self.dos)
    
    # 
    # Hacemos lo mismo para la division
    #
    def test13DivisionDeEnteroPorFraccion(self):
        self.assertEqual(self.cincoMedios,self.uno/self.dosQuintos)
    
    def test14DivisionDeFraccionPorEntero(self):
        self.assertEqual(self.dosVeinticincoavos,self.dosQuintos/self.cinco)
    
    # 
    # Ahora si empezamos con problemas de reduccion de fracciones
    #
    def test15UnaFraccionPuedeSerIgualAUnEntero(self):
        self.assertEquals(self.dos,self.cuatroMedios)
    
    def test42DeberiamosReducirAlCrearFracciones(self):    
        ##lo agregue yo, despues lo sacamos, tomi p, esto es prueba de que no pasarian asi. 
        assert(self.dos.__eq__(Fraccion(4,2))== False)
        assert(Fraccion(4,2).__eq__(self.dos)==False)

    def test16LasFraccionesAparentesSonIguales(self):
        self.assertEquals(self.unMedio,self.dosCuartos)
        #
        # Las fracciones se reducen utilizando el maximo comun divisor (mcd)
        # Por lo tanto, para a/b, sea c = mcd (a,b) => a/b reducida es:
        # (a/c) / (b/c).
        # 
        # Por ejemplo: a/b = 2/4 entonces c = 2. Por lo tanto 2/4 reducida es:
        # (2/2) / (4/2) = 1/2
        # 
        # Para obtener el mcd pueden usar el algoritmo de Euclides que es:
        # 
        # mcd (a,b) = 
        #         si b = 0 --> a
        #         si b != 0 -->mcd(b, restoDeDividir(a,b))
        #     
        # Ejemplo:
        # mcd(2,4) ->
        # mcd(4,restoDeDividir(2,4)) ->
        # mcd(4,2) ->
        # mcd(2,restoDeDividir(4,2)) ->
        # mcd(2,0) ->
        # 2
        #
    
    def test17LaSumaDeFraccionesPuedeDarEntero(self):
        self.assertEquals (self.uno,self.unMedio+self.unMedio)

    def test18LaMultiplicacionDeFraccionesPuedeDarEntero(self):
        self.assertEquals(self.dos,self.cuatro*self.unMedio)

    def test19LaDivisionDeEnterosPuedeDarFraccion(self):
        self.assertEquals(self.unMedio, self.dos/self.cuatro)

    def test20LaDivisionDeFraccionesPuedeDarEntero(self):
        self.assertEquals(self.uno, self.unMedio/self.unMedio)
    
    def test21NoSePuedeDividirEnteroPorCero(self):
        try:
            self.uno/self.cero
            self.fail()
        except Exception as e:
            self.assertEquals(self.descripcionDeErrorDeNoSePuedeDividirPorCero(),e.message)

    def test22NoSePuedeDividirFraccionPorCero(self):
        try:
            self.unQuinto/self.cero
            self.fail()
        except Exception as e:
            self.assertEquals(self.descripcionDeErrorDeNoSePuedeDividirPorCero(),e.message)

    # Este test puede ser redundante dependiendo de la implementacion realizada 
    def test23NoSePuedeCrearFraccionConDenominadorCero(self):
        try:
            self.crearFraccionCon(self.uno,self.cero)
            self.fail()
        except Exception as e:
            self.assertEquals(self.descripcionDeErrorDeNoSePuedeDividirPorCero(),e.message)

    def crearFraccionCon(self, numerador, denominador): 
        return numerador/denominador
    
    def descripcionDeErrorDeNoSePuedeDividirPorCero(self):
        #Tratar de que la implementacion de este metodo utilice el mensaje definido en alguna de las clase de numero
        return Numero.DESCRIPCION_DE_ERROR_DE_DIVISION_POR_CERO
    
if __name__ == "__main__":
    unittest.main()
    
