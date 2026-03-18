package SLotmaschine;
// Api zwischen java methoden und flask server
public class SlotsApi {
    public static void main(String[] args) {
        SlotsLogik slots = new SlotsLogik();
        // festlegung der auszugebenden werte
        int win1 = slots.final1();
        int win2 = slots.final2();
        int win3 = slots.final3();
        int payout = slots.Ausgabe(win1, win2, win3);
        // formatierung der werte für die ausgabe
        String json = String.format(
            "{\"slot1\":%d,\"slot2\":%d,\"slot3\":%d,\"payout\":%d}",
            win1, win2, win3, payout
        );
        // ausgabe der werte
        System.out.println(json);
    }
}