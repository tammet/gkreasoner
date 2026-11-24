import fr.lirmm.graphik.DEFT.core.DefeasibleKB;
import fr.lirmm.graphik.graal.api.core.Atom;
import java.util.Iterator;

/** load a DLGP file, saturate, print the entailment status of each query atom given as argument */
public class DeftRun {
  public static void main(String[] args) throws Exception {
    long t0 = System.currentTimeMillis();
    DefeasibleKB kb = new DefeasibleKB(args[0]);
    kb.saturate();
    long t1 = System.currentTimeMillis();
    for (int i = 1; i < args.length; i++) {
      var it = kb.getAtomsSatisfiyingAtomicQuery("? :- " + args[i] + ".").iterator();
      if (!it.hasNext()) { System.out.println(args[i] + " : NOT_ENTAILED (no atom)"); continue; }
      Atom atom = it.next();
      int e = kb.EntailmentStatus(atom);
      String s = e == DefeasibleKB.NOT_ENTAILED ? "NOT_ENTAILED" : e == DefeasibleKB.STRICTLY_ENTAILED ? "STRICTLY_ENTAILED" : "DEFEASIBLY_ENTAILED";
      System.out.println(args[i] + " : " + s);
    }
    long t2 = System.currentTimeMillis();
    System.out.println("saturate_ms=" + (t1 - t0) + " query_ms=" + (t2 - t1));
  }
}
