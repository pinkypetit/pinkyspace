import arcade
import random
import math
import time

#defino ventana;
ancho = 800                                                                                    #este sera el ancho de la pantalla 
alto = 800                                                                                    #este sera el alto de la pantalla

#defino caracteristicas de los sprites (velocidades)
velocidad_nave = 15                                                                              #esta es la velocidad bace de la nave del jugador
velocidad_angular = 8                                                                           #esta es la velocidad angular base de la nave de jugador                                                                    
velocidad_bala = 30                                                                            #esta es la velocidad a la que viajan las balas
velocidad_inicial_enemigos = 1                                                                #esta es la volocidad minima que pueden tener los enemigos


desarollador = 0                                                                                #cambia este valor a 1 para activar opciones de desarrollador (colaider vicibles )




#
def telon(color):
        arcade.draw_lrtb_rectangle_filled(
                0*ancho,
                .13*ancho,
                1*alto,
                0*alto,
                color
        )            
        arcade.draw_lrtb_rectangle_filled(
                .87*ancho,
                1*ancho,
                1*alto,
                0*alto,
                color
        )
        arcade.draw_lrtb_rectangle_filled(
                0*ancho,
                1*ancho,
                .13*alto,
                0*alto,
                color
        )            
        arcade.draw_lrtb_rectangle_filled(
                0*ancho,
                1*ancho,
                1*alto,
                .87*alto,
                color
        )






class DibujaImagen(arcade.Window):

        def __init__(self):
                #asuntos globales;
                super().__init__(ancho,alto,'Pinky.Space', False,True)                              #creo la ventana.
                arcade.set_background_color(arcade.color.BITTERSWEET)                               #defino el color del fondo.
                self.choques = 0

                self.juego = 0
                self.menu = 1
                self.momento = 0
                self.fin = 0

                #limito la tasa de frames
                self.set_update_rate(1 / 30)

                self.creditos = arcade.Sprite("imagenes/creditos.png",.22 )     
                self.creditos.center_x=alto //2
                self.creditos.center_y=ancho//2
                self.pagina_1 = arcade.Sprite("imagenes/instruciones_1.png",.47)
                self.pagina_1.center_y=ancho//2
                self.pagina_1.center_x=alto//2
                self.pagina_2 = arcade.Sprite("imagenes/instruciones_2.png",.47)
                self.pagina_2.center_y=ancho//2
                self.pagina_2.center_x=alto//2
                self.pagina_3 = arcade.Sprite("imagenes/instruciones_3.png",.47)
                self.pagina_3.center_y=ancho//2
                self.pagina_3.center_x=alto//2
                self.pagina_4 = arcade.Sprite("imagenes/instruciones_4.png",.47)
                self.pagina_4.center_y=ancho//2
                self.pagina_4.center_x=alto//2
                self.pagina_5 = arcade.Sprite("imagenes/instruciones_5.png",.47)
                self.pagina_5.center_y=ancho//2
                self.pagina_5.center_x=alto//2
                self.victoria = arcade.Sprite("imagenes/victoria.png",.7)
                self.victoria.center_y=ancho//2
                self.victoria.center_x=alto//2
                self.gameover = arcade.Sprite("imagenes/gameover.png",.7)
                self.gameover.center_y=ancho//2
                self.gameover.center_x=alto//2


                self.pagina = 0
                self.creditos_on = 0
                #defino y agrego la nave a la lista de personajes;
                self.nave = arcade.Sprite('imagenes/nave_BALLBLUE.png', .1)                         #imagen del sprite.

                self.recarga = arcade.Sprite('imagenes/circulo.png', .1)
                self.recarga.center_y = random.randint(.150*alto,(alto -.150*alto))                                                      #posicion vertical.
                self.recarga.center_x = random.randint(.150*alto,(alto -.150*alto))                                                     #posicion horizontal.


                self.falta_de_enemigos = False
                self.arriba = False
                self.abajo = False
                self.reloj = False
                self.anti_reloj = False
                self.derecha = False
                self.izquerda = False

                self.level = 1 
                self.mejor_puntaje = 0
                self.puntos = 0



                #musica
                self.musica = arcade.Sound('sc/musica.mp3', True)
                self.musica.play(volume = .3 + .7*self.choques)
                self.disparo= arcade.Sound ("sc/disparo.wav",False)
                self.explocion= arcade.Sound ("sc/explosion.wav",False)












        #creo los elementos moviles;
        def setup(self):

                self.balas = arcade.SpriteList() 
                self.balasenemigas = arcade.SpriteList()
                self.nave.center_y = alto // 2                                                      #posicion vertical.
                self.nave.center_x = ancho // 2                                                     #posicion horizontal.
                self.nave.angle = 0                                                                 #inclinacion de la nave.


                self.enemigos_list = arcade.SpriteList() 
                self.enemigos_list_2 = arcade.SpriteList() 
                self.enemigos_list_3 = arcade.SpriteList() 



                self.explotar = 0



                # leer colaiders
                self.colaiders = arcade.tilemap.read_tmx('colaiders.tmx')                           #archivo en tmx contiene una matriz con la informacion de los colaiders (ver archivo 'colaider.tmx').
                #defino y aplico el colaider 'borde';
                self.borde = arcade.SpriteList(use_spatial_hash=True)                               # 'use_spatial_hash=True' es usado para optimisar los objetos que no se mueven.
                self.borde.extend(arcade.tilemap.process_layer(self.colaiders, 'Bordes'))           # defino que onjeto demntro de 'colaiders.tmx' es el que interactuara con las fisicas
                #agrego las coliciones entre 'nave ' y 'borde';
                self.fisica = arcade.PhysicsEngineSimple(self.nave, self.borde)

        #dibujo los elementos
        def on_draw(self):
                #inicio dibujo
                arcade.start_render()


                if self.menu == 1:
                        self.fondomenu.draw()

                if self.pagina == 1:
                        self.pagina_1.draw()

                if self.pagina == 2 :
                        self.pagina_2.draw()  

                if self.pagina == 3 :
                        self.pagina_3.draw()
                if self.pagina == 4 :
                        self.pagina_4.draw()
                if self.pagina == 5 :
                        self.pagina_5.draw()
                        
                if self.creditos_on == 1:
                        self.creditos.draw()  




                if self.juego == 1:
                        arcade.draw_lrtb_rectangle_filled(
                                .13*ancho,
                                .87*ancho,
                                .87*alto,
                                .13*alto,
                                arcade.color.BABY_POWDER
                        )

                        arcade.draw_lrtb_rectangle_filled(
                                .14*ancho,
                                .86*ancho,
                                .86*alto,
                                .14*alto,
                                
                                (137, 207, 240, 70)
                        )
                        arcade.draw_lrtb_rectangle_filled(
                                .15*ancho,
                                .85*ancho,
                                .85*alto,
                                .15*alto,
                                
                                arcade.color.BABY_POWDER
                        )

                        # #vidas;
                        # self.y = [2,2,2,1,0,0,0,1]
                        # self.x = [0,1,2,0,2,0,1,2]
                        # for i in self.x:
                        #       for j in self.y:
                        #             arcade.draw_lrtb_rectangle_filled(
                        #                   (.14+i*.17)*ancho,
                        #                   (.14+((i+1)*.17))*ancho,
                        #                   (.14+(j+1)*.17)*alto,
                        #                   (.14+(j*.17))*alto,
                        #                   self.color
                        #             )                



                        #vida numero 1;
                        if  1 <= self.vidas:
                                arcade.draw_lrtb_rectangle_filled(
                                        .14*ancho,
                                        .325*ancho,
                                        .86*alto,
                                        .675*alto,
                                        
                                        self.color
                                )                
                        #vida numero 2;d
                        if  2 <= self.vidas:
                                arcade.draw_lrtb_rectangle_filled(
                                        .335*ancho,
                                        .665*ancho,
                                        .86*alto,
                                        .675*alto,
                                        
                                        self.color
                                )  
                                
                        #vida numero 3;
                        if  3 <= self.vidas:
                                arcade.draw_lrtb_rectangle_filled(
                                        .675*ancho,
                                        .86*ancho,
                                        .86*alto,
                                        .675*alto,
                                        
                                        self.color
                                )                                           
                        #vida numero 4;
                        if  4 <= self.vidas:
                                arcade.draw_lrtb_rectangle_filled(
                                        .675*ancho,
                                        .86*ancho,
                                        .665*alto,
                                        .335*alto,
                                        
                                        self.color
                                )         
                        #vida numero 5;
                        if  5 <= self.vidas:
                                arcade.draw_lrtb_rectangle_filled(
                                        .675*ancho,
                                        .86*ancho,
                                        .325*alto,
                                        .14*alto,
                                        
                                        self.color
                                )  
                        #vida numero 6;
                        if  6 <= self.vidas:
                                arcade.draw_lrtb_rectangle_filled(
                                        .335*ancho,
                                        .665*ancho,
                                        .325*alto,
                                        .14*alto,
                                        
                                        self.color
                                )  
                        #vida numero 7;
                        if  7 <= self.vidas:
                                arcade.draw_lrtb_rectangle_filled(
                                        .14*ancho,
                                        .325*ancho,
                                        .325*alto,
                                        .14*alto,
                                        
                                        self.color
                                )        
                        #vida numero 8;
                        if  8 <= self.vidas:
                                arcade.draw_lrtb_rectangle_filled(
                                        .14*ancho,
                                        .325*ancho,
                                        .665*alto,
                                        .335*alto,
                                        
                                        self.color
                                )  





                        arcade.draw_lrtb_rectangle_filled(
                                .15*ancho,
                                .85*ancho,
                                .85*alto,
                                .15*alto,
                                arcade.color.BABY_POWDER
                        )

                        self.balas.draw()
                        self.balasenemigas.draw()
                        self.nave.draw()
                        self.recarga.draw()
                        self.enemigos_list.draw()
                        self.enemigos_list_2.draw()
                        self.enemigos_list_3.draw()


                        if desarollador == 1 :
                                self.bala.draw_hit_box()  
                                # self.nave_enemiga.draw_hit_box()
                                self.nave.draw_hit_box()
                        
                        #telon
                        if desarollador == 0:
                                if self.level == 1 :
                                        telon((244, 194, 194))
                                if self.level == 2 :
                                        telon((151, 233, 159))
                                if self.level == 3 :
                                        telon((165, 50, 105))
                        elif desarollador == 1:
                                if self.level == 1 :
                                        telon((244, 194, 194,0))
                                if self.level == 2 :
                                        telon((151, 233, 159,0))
                                if self.level == 3 :
                                        telon((165, 50, 105,0))
                                        




                        arcade.draw_text((f'nivel: {self.level}'), 50, alto - 50, arcade.color.WHITE,24)  
                        arcade.draw_text((f'puntos: {self.puntos}'), 50, alto - 80, arcade.color.WHITE,24)
                        arcade.draw_text((f'record: {self.mejor_puntaje}'), 50, alto - 110, arcade.color.WHITE,24)
                        arcade.draw_text((f'sobrevivir: {100-self.explotar}%'), ancho- 250, alto - 50, arcade.color.WHITE,24)
                        if 15 <= self.puntos and self.level == 3:
                                arcade.draw_text((f'ganaste '), 50, alto - 130, arcade.color.WHITE,24)

                        if self.vidas <= 0 and self.puntos < 15:
                                arcade.draw_lrtb_rectangle_filled(
                                        0*ancho,
                                        1*ancho,
                                        1*alto,
                                        0*alto,
                                        (244, 194, 194)
                                )
                                self.gameover.draw()
                                self.fin = 1

                        if self.vidas <= 0 and 15 <= self.puntos :
                                arcade.draw_lrtb_rectangle_filled(
                                        0*ancho,
                                        1*ancho,
                                        1*alto,
                                        0*alto,
                                        (244, 194, 194)
                                )
                                self.fin = 1
                                self.victoria.draw()                               


        def on_update(self, delta_time):
                self.fondomenu=arcade.Sprite("imagenes/menu.png",.50 + .03*math.sin(self.momento))
                self.fondomenu.center_x=alto //2
                self.fondomenu.center_y=ancho//2
                self.enemigos_list.update()
                self.enemigos_list_2.update()
                self.enemigos_list_3.update()
                self.fisica.update()

                choques = arcade.check_for_collision_with_list(self.nave, self.enemigos_list ) + arcade.check_for_collision_with_list(self.nave, self.enemigos_list_2 ) + arcade.check_for_collision_with_list(self.nave, self.enemigos_list_3 ) + arcade.check_for_collision_with_list(self.nave, self.balasenemigas )
                self.vidas = 8 - self.choques
                recarga = arcade.check_for_collision(self.nave,self.recarga)

                if recarga:
                        self.recarga.center_y = random.randint(150,(alto -.150*alto))                                                      #posicion vertical.
                        self.recarga.center_x = random.randint(150,(alto -.150*alto))                                                     #posicion horizontal.
                        self.explotar = 0


                if self.level == 1 :
                        self.velocidad_enemigos = velocidad_inicial_enemigos*1
                        self.color = (137, 207, 240)
                if self.level == 2 :
                        self.velocidad_enemigos = velocidad_inicial_enemigos*1.7
                        self.color = (109, 203, 191)
                if self.level == 3 :
                        self.velocidad_enemigos = velocidad_inicial_enemigos*2
                        self.color = (86, 131, 204)

                self.nave.change_y  = 0
                self.nave.change_x  = 0
                self.nave.change_angle = 0

                if self.arriba and not self.abajo  :
                        self.nave.change_y = velocidad_nave
                elif  self.abajo and not self.arriba:
                        self.nave.change_y   =   -velocidad_nave       
                if self.izquerda and not self.derecha:
                        self.nave.change_x  = -velocidad_nave
                elif not self.izquerda and self.derecha:
                        self.nave.change_x = velocidad_nave
                if self.anti_reloj and not self.reloj:
                        self.nave.change_angle = velocidad_angular
                elif not self.anti_reloj and self.reloj:
                        self.nave.change_angle = - velocidad_angular 


                for bala in self.balas:
                        self.bajas = arcade.check_for_collision_with_list(bala, self.enemigos_list )
                        for baja in self.bajas:
                                bala.remove_from_sprite_lists()
                                self.puntos += 1
                                if self.mejor_puntaje < self.puntos:
                                        self.mejor_puntaje += 1
                                for baja in self.bajas:
                                        baja.remove_from_sprite_lists()
                for bala in self.balas:
                        self.bajas = arcade.check_for_collision_with_list(bala, self.enemigos_list_2 )
                        for baja in self.bajas:
                                bala.remove_from_sprite_lists()
                                self.puntos += 1
                                if self.mejor_puntaje < self.puntos:
                                        self.mejor_puntaje += 1                                
                                for baja in self.bajas:
                                        baja.remove_from_sprite_lists()
                for bala in self.balas:
                        self.bajas = arcade.check_for_collision_with_list(bala, self.enemigos_list_3 )
                        for baja in self.bajas:
                                bala.remove_from_sprite_lists()
                                self.puntos += 1
                                if self.mejor_puntaje < self.puntos:
                                        self.mejor_puntaje += 1
                                for baja in self.bajas:
                                        baja.remove_from_sprite_lists()

                for choque in choques:
                        self.choques += 1
                        self.setup()

                if self.juego == 1:
                        for nave_enemiga in self.enemigos_list:  
                                if (self.nave.center_x)-(nave_enemiga.center_x) <= 0 :
                                        nave_enemiga.angle = (180/math.pi)*math.acos((
                                        ((self.nave.center_y)-(nave_enemiga.center_y))/
                                        math.sqrt(((self.nave.center_y)-(nave_enemiga.center_y))**2 + 
                                        ((self.nave.center_x)-(nave_enemiga.center_x))**2)   ))                  #inclinacion de la nave.

                                elif (self.nave.center_x)-(nave_enemiga.center_x) > 0:
                                        nave_enemiga.angle = -(180/math.pi)*math.acos((
                                        ((self.nave.center_y)-(nave_enemiga.center_y))/
                                        math.sqrt(((self.nave.center_y)-(nave_enemiga.center_y))**2 + 
                                        ((self.nave.center_x)-(nave_enemiga.center_x))**2)   ))                                     
                                        
                                if (self.nave.center_y) != (nave_enemiga.center_y):
                                        nave_enemiga.center_y += (self.velocidad_enemigos * (math.sin(nave_enemiga.angle) )
                                        +2*abs((self.nave.center_y)-(nave_enemiga.center_y))/
                                        ((self.nave.center_y)-(nave_enemiga.center_y))
                                        )
                                if (self.nave.center_x) != (nave_enemiga.center_x):
                                        nave_enemiga.center_x += (self.velocidad_enemigos * (math.cos(nave_enemiga.angle))  
                                        +2*abs((self.nave.center_x)-(nave_enemiga.center_x))/
                                        ((self.nave.center_x)-(nave_enemiga.center_x))
                                )    
                        for nave_enemiga in self.enemigos_list_2:  
                                if math.sqrt(((self.nave.center_x)-(nave_enemiga.center_x))**2+((self.nave.center_y)-(nave_enemiga.center_y))**2) == 200 or math.sqrt(((self.nave.center_x)-(nave_enemiga.center_x))**2+((self.nave.center_y)-(nave_enemiga.center_y))**2) == 300 or math.sqrt(((self.nave.center_x)-(nave_enemiga.center_x))**2+((self.nave.center_y)-(nave_enemiga.center_y))**2) == 150:
                                        self.potenciador = 3
                                else:
                                        self.potenciador = 1
                                if (self.nave.center_x)-(nave_enemiga.center_x) <= 0 :
                                        nave_enemiga.angle = (180/math.pi)*math.acos((
                                        ((self.nave.center_y)-(nave_enemiga.center_y))/
                                        math.sqrt(((self.nave.center_y)-(nave_enemiga.center_y))**2 + 
                                        ((self.nave.center_x)-(nave_enemiga.center_x))**2)   ))                  #inclinacion de la nave.

                                elif (self.nave.center_x)-(nave_enemiga.center_x) > 0:
                                        nave_enemiga.angle = -(180/math.pi)*math.acos((
                                        ((self.nave.center_y)-(nave_enemiga.center_y))/
                                        math.sqrt(((self.nave.center_y)-(nave_enemiga.center_y))**2 + 
                                        ((self.nave.center_x)-(nave_enemiga.center_x))**2)   ))                                     
                                        
                                if (self.nave.center_y) != (nave_enemiga.center_y):
                                        nave_enemiga.center_y += (self.velocidad_enemigos * (math.sin(nave_enemiga.angle) )
                                        +2*self.potenciador*abs((self.nave.center_y)-(nave_enemiga.center_y))/
                                        ((self.nave.center_y)-(nave_enemiga.center_y))
                                        )
                                if (self.nave.center_x) != (nave_enemiga.center_x):
                                        nave_enemiga.center_x += (self.velocidad_enemigos * (math.cos(nave_enemiga.angle))  
                                        +2*self.potenciador*abs((self.nave.center_x)-(nave_enemiga.center_x))/
                                        ((self.nave.center_x)-(nave_enemiga.center_x))
                                )    
                        for nave_enemiga in self.enemigos_list_3:  
                                if (self.nave.center_x)-(nave_enemiga.center_x) <= 0 :
                                        nave_enemiga.angle = (180/math.pi)*math.acos((
                                        ((self.nave.center_y)-(nave_enemiga.center_y))/
                                        math.sqrt(((self.nave.center_y)-(nave_enemiga.center_y))**2 + 
                                        ((self.nave.center_x)-(nave_enemiga.center_x))**2)   ))                  #inclinacion de la nave.

                                elif (self.nave.center_x)-(nave_enemiga.center_x) > 0:
                                        nave_enemiga.angle = -(180/math.pi)*math.acos((
                                        ((self.nave.center_y)-(nave_enemiga.center_y))/
                                        math.sqrt(((self.nave.center_y)-(nave_enemiga.center_y))**2 + 
                                        ((self.nave.center_x)-(nave_enemiga.center_x))**2)   ))                                     
                                        
                                if (self.nave.center_y) != (nave_enemiga.center_y):
                                        nave_enemiga.center_y += (self.velocidad_enemigos * (math.sin(nave_enemiga.angle) )
                                        +2*abs((self.nave.center_y)-(nave_enemiga.center_y))/
                                        ((self.nave.center_y)-(nave_enemiga.center_y))
                                        )
                                if (self.nave.center_x) != (nave_enemiga.center_x):
                                        nave_enemiga.center_x += (self.velocidad_enemigos * (math.cos(nave_enemiga.angle))  
                                        +2*abs((self.nave.center_x)-(nave_enemiga.center_x))/
                                        ((self.nave.center_x)-(nave_enemiga.center_x))
                                )    
                                if 195<= math.sqrt(((nave_enemiga.center_x)-(self.nave.center_x))**2+((nave_enemiga.center_y)-(self.nave.center_y))**2) <= 200:

                                        bala = arcade.Sprite('imagenes/path34809.png', .03)                                    #imagen del sprite.
                                        bala.center_y = nave_enemiga.center_y                                             #posicion vertical.
                                        bala.center_x = nave_enemiga.center_x                                             #posicion horizontal.
                                        bala.angle = nave_enemiga.angle      
                                        self.balasenemigas.append(bala)



                if self.puntos < 5:
                        self.level = 1
                elif 5 <= self.puntos < 10:
                        self.level =  2
                elif 10 <= self.puntos :
                        self.level =  3

                
                if self.level == 1 and (len (self.enemigos_list) + len (self.enemigos_list_2) + len (self.enemigos_list_3) ) < 3 :
                        nave_enemiga = arcade.Sprite('imagenes/enemigo.png', .08)                      #imagen del sprite.
                        nave_enemiga.center_y = random.randint(0,.150*alto) + random.randint(0,1)*(alto -.150*alto)         #posicion vertical.
                        nave_enemiga.center_x = random.randint(0,.150*alto) + random.randint(0,1)*(alto -.150*alto)        #posicion horizontal.                
                        #agrego la nave enemiga basica;
                        self.enemigos_list.append(nave_enemiga)
                        self.falta_de_enemigos = False
                self.random = random.randint(0,2)
                if self.level == 2 and (len (self.enemigos_list) + len (self.enemigos_list_2) + len (self.enemigos_list_3) ) < 6:
                        if self.random == 0 or self.random == 1:
                                nave_enemiga = arcade.Sprite('imagenes/enemigo.png', .08)                      #imagen del sprite.
                                nave_enemiga.center_y = random.randint(0,.150*alto) + random.randint(0,1)*(alto -.150*alto)         #posicion vertical.
                                nave_enemiga.center_x = random.randint(0,.150*alto) + random.randint(0,1)*(alto -.150*alto)        #posicion horizontal.                
                                #agrego la nave enemiga basica;
                                self.enemigos_list.append(nave_enemiga)
                        elif self.random == 2 :
                                nave_enemiga_2 = arcade.Sprite('imagenes/enemigo_2.png', .08)                      #imagen del sprite.
                                nave_enemiga_2.center_y = random.randint(0,.150*alto) + random.randint(0,1)*(alto -.150*alto)         #posicion vertical.
                                nave_enemiga_2.center_x = random.randint(0,.150*alto) + random.randint(0,1)*(alto -.150*alto)        #posicion horizontal.                
                                #agrego la nave enemiga rapida;
                                self.enemigos_list_2.append(nave_enemiga_2)

                if self.level == 3 and (len (self.enemigos_list) + len (self.enemigos_list_2) + len (self.enemigos_list_3) ) < 7:
                        if self.random == 0 :
                                nave_enemiga = arcade.Sprite('imagenes/enemigo.png', .08)                      #imagen del sprite.
                                nave_enemiga.center_y = random.randint(0,.150*alto) + random.randint(0,1)*(alto -.150*alto)         #posicion vertical.
                                nave_enemiga.center_x = random.randint(0,.150*alto) + random.randint(0,1)*(alto -.150*alto)        #posicion horizontal.                
                                #agrego la nave enemiga basica;
                                self.enemigos_list.append(nave_enemiga)
                        elif self.random == 1 :
                                nave_enemiga_2 = arcade.Sprite('imagenes/enemigo_2.png', .08)                      #imagen del sprite.
                                nave_enemiga_2.center_y = random.randint(0,.150*alto) + random.randint(0,1)*(alto -.150*alto)         #posicion vertical.
                                nave_enemiga_2.center_x = random.randint(0,.150*alto) + random.randint(0,1)*(alto -.150*alto)        #posicion horizontal.                
                                #agrego la nave enemiga rapida;
                                self.enemigos_list_2.append(nave_enemiga_2)
                        elif self.random == 2 :
                                nave_enemiga_3 = arcade.Sprite('imagenes/enemigo_3.png', .08)                      #imagen del sprite.
                                nave_enemiga_3.center_y = random.randint(0,.150*alto) + random.randint(0,1)*(alto -.150*alto)         #posicion vertical.
                                nave_enemiga_3.center_x = random.randint(0,.150*alto) + random.randint(0,1)*(alto -.150*alto)        #posicion horizontal.  
                         
                                            
                                #agrego la nave enemiga 3;
                                self.enemigos_list_3.append(nave_enemiga_3)



                #agrego la bala a la lista de balas;
                for bala in self.balas:
                        bala.center_y = bala.center_y + math.cos((math.pi/180)*bala.angle)*velocidad_bala
                        bala.center_x = bala.center_x - math.sin((math.pi/180)*bala.angle)*velocidad_bala 

                for bala in self.balasenemigas:
                        bala.center_y = bala.center_y + math.cos((math.pi/180)*bala.angle)*velocidad_bala
                        bala.center_x = bala.center_x - math.sin((math.pi/180)*bala.angle)*velocidad_bala


                self.momento = self.momento + 0.01  




        def on_key_press(self, key , modifiers):
                if self.juego == 1:
                        if key == arcade.key.UP or key == arcade.key.W:
                                self.arriba =  True 
                        if key == arcade.key.DOWN or key == arcade.key.S:
                                self.abajo =  True               
                        if key == arcade.key.LEFT or key == arcade.key.A:
                                self.izquerda = True 
                        if key == arcade.key.RIGHT or key == arcade.key.D:
                                self.derecha =  True 
                        if key == arcade.key.Q or key == arcade.key.KEY_7 or key == arcade.key.NUM_7:
                                self.anti_reloj = True 
                        if key == arcade.key.E or key == arcade.key.KEY_9 or key == arcade.key.NUM_9:
                                self.reloj = True 
                        if key == arcade.key.C :
                                self.nave.change_angle = 180
                if key == arcade.key.SPACE and self.juego == 1:
                        bala = arcade.Sprite('imagenes/nave_BABYBLUE.png', .03)                              #imagen del sprite.
                        bala.center_y = self.nave.center_y                                             #posicion vertical.
                        bala.center_x = self.nave.center_x                                             #posicion horizontal.
                        bala.angle = self.nave.angle   
                        self.explotar += 1   
                        self.balas.append(bala)
                        prob = random.randint(0,100)
                        if prob < self.explotar:
                                self.choques += 1
                                self.setup()
                                self.explocion.play(volume = .3)
                        else:
                                self.disparo.play(volume = .3)


                if key == arcade.key.A  and self.pagina == 1:
                        self.pagina = 4
                elif key == arcade.key.A  and self.pagina == 2:
                        self.pagina = 1
                elif key == arcade.key.A  and self.pagina == 3:
                        self.pagina = 2
                elif key == arcade.key.A  and self.pagina == 4:
                        self.pagina = 3
                elif key == arcade.key.A  and self.pagina == 5:
                        self.pagina = 4

                elif key == arcade.key.D  and self.pagina == 1:
                        self.pagina = 2
                elif key == arcade.key.D  and self.pagina == 2:
                        self.pagina = 3
                elif key == arcade.key.D  and self.pagina == 3:
                        self.pagina = 4
                elif key == arcade.key.D  and self.pagina == 4:
                        self.pagina = 5
                elif key == arcade.key.D  and self.pagina == 5:
                        self.pagina = 1

                if key == arcade.key.ESCAPE and self.pagina != 0:
                        self.pagina = 0
                        self.menu = 1

                if key == arcade.key.ESCAPE and self.creditos_on == 1:
                        self.creditos_on = 0
                        self.menu = 1


        def on_key_release(self, key, modifiers):
                if key == arcade.key.UP or key == arcade.key.W:
                        self.arriba =  False 
                if key == arcade.key.DOWN or key == arcade.key.S:
                        self.abajo =   False               
                if key == arcade.key.LEFT or key == arcade.key.A:
                        self.izquerda = False 
                if key == arcade.key.RIGHT or key == arcade.key.D:
                        self.derecha =  False 
                if key == arcade.key.Q or key == arcade.key.KEY_7 or key == arcade.key.NUM_7 :
                        self.anti_reloj = False 
                if key == arcade.key.E or key == arcade.key.KEY_9 or key == arcade.key.NUM_9:
                        self.reloj = False 
                if key == arcade.key.ENTER:
                        self.juego = 1
                        self.menu = 0
                if key == arcade.key.ENTER and self.fin == 1:
                        self.choques = 0
                        self.puntos = 0
                        self.setup()

                if key == arcade.key.C and self.menu == 1:
                        self.creditos_on = 1
                        self.menu = 0

                if key == arcade.key.I and self.menu == 1:
                        
                        self.pagina =  1
                        self.menu = 0





def main():
        ventana = DibujaImagen()
        ventana.setup()
        arcade.run()

main()