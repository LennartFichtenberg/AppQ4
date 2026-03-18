package SLotmaschine;

import java.util.Random;

public class SlotsLogik {





  
  int playerMoney = 10000;

  /*public slots(int startMoney) {
    

      this.playerMoney = startMoney; // nimmt wert der übergeben wurde

   
  }     */    
   

  // Kontrollen

  boolean pressed = false;
  boolean SoundCheck = true;
  boolean cheat = false;
  boolean fast = false;
  
  boolean final1  = false;
  boolean final2  = false;
  boolean final3  = false;
  
  
  
  int ani;

  Random random = new Random();

  int durchlaufSlot1 = 0;
  int durchlaufSlot2 = 0;
  int durchlaufSlot3 = 0;

  // Spatere Kontrolle ob sieg
  

  int wahscheinlichkeit = 8; // zwischen 1 und 8 (bis zu acht symbolen)     randomizer animatrion
  
  int wahrscheinlichkeitenfinal = 100; //festlegung wahrscheinlichkeiten
  

  // Sound
  

  //  Bildschirm erstellung
    public int auswahl ()  {
        int r = random.nextInt(wahrscheinlichkeitenfinal); // 0..99
             
        int win;  

          // Range-Verteilung:
          // 0-4   : Seven (5%)
          // 5-24  : Banane (20%)
          // 25-42 : Erdbeere (18%)
          // 43-57 : Kirsche (15%)
          // 58-72 : Orange (15%)
          // 73-84 : Traube (12%)
          // 85-94 : Wassermelone (10%)
           // 95-99 : Zitrone (5%)

          if (r < 5) {
            win = 0;
          }
            else if (r < 25) {
              win = 1;
            }
              else if (r < 43) {
                win = 2;
              }
                else if (r < 58) {;
                  win = 3;
                }
                  else if (r < 73) {
                    win = 4;
                  }
                    else if (r < 85) {     
                      win = 5;
                    }
                      else if (r < 95) {
                        win = 6;
                      }
                      else {
                        win = 7;
                      }
                
    
                 return win;
      }
  
        
        
  public int final1 ()  {
             
        int win1 = this.auswahl(); 
         return  win1; 
          
        }
          
              
            
      
  public int final2 ()  {
      int win2 = this.auswahl();
      return  win2;    
                      }

          
          
        
  public int final3 ()         {
    
    int win3 = this.auswahl();
    return  win3;
    }
         

            // kontrolle ob gewonnen
  public int Ausgabe (int win1, int win2, int win3) {
            
           boolean triple = (win1 == win2 && win2 == win3);
           boolean pair   = !triple && (win1 == win2 || win1 == win3 || win2 == win3);

           int payout = 0;

    // =========================
    // 3 GLEICHE (JACKPOT)
    // =========================
           if (triple) {

         

             switch (win1) {
              case 0: payout = 800; break; // Seven (selten)
              case 1: payout = 150; break; // Banane (häufig)
              case 2: payout = 180; break; // Erdbeere
              case 3: payout = 220; break; // Kirsche
              case 4: payout = 220; break; // Orange
              case 5: payout = 300; break; // Traube
              case 6: payout = 380; break; // Wassermelone
              case 7: payout = 800; break; // Zitrone (selten)
            }

            
            }

          // =========================
          // GENAU 2 GLEICHE
          // =========================
            else if (pair) {
          
              int pairSymbol;

              if (win1 == win2) pairSymbol = win1;
               else if (win1 == win3) pairSymbol = win1;
                else pairSymbol = win2; // win2 == win3

              switch (pairSymbol) {
                case 0: payout = 25; break; // Seven
                case 1: payout = 10; break; // Banane
                case 2: payout = 12; break; // Erdbeere
                case 3: payout = 15; break; // Kirsche
                 case 4: payout = 15; break; // Orange
                 case 5: payout = 18; break; // Traube
                case 6: payout = 20; break; // Wassermelone
                 case 7: payout = 25; break; // Zitrone
                      }
                      }

          // =========================
          // AUSZAHLEN
          // =========================
          if (payout > 0) {
          //playerMoney += payout;
          
             
             return  payout;
                                                      }

            

            return  payout; 
         }
 
       

    
           
  // Anfang Methoden

    public void Cheaten(boolean cheat) {
    // wahscheinlichkeit runter stellen

    if (cheat == false) {
      wahrscheinlichkeitenfinal = 1;
      
      
      
      System.out.println("Saihde Kebab Scherrif");
      cheat = true;
    }

    else {
      wahrscheinlichkeitenfinal = 100;
      
      cheat = false;
    }
  }

 
  

  

  public static void main(String[] args) {
    

  }
  // Ende Methoden
}