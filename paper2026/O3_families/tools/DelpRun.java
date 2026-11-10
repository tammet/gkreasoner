import org.tweetyproject.arg.delp.parser.DelpParser;
import org.tweetyproject.arg.delp.reasoner.DelpReasoner;
import org.tweetyproject.arg.delp.semantics.DelpAnswer;
import org.tweetyproject.arg.delp.semantics.GeneralizedSpecificity;
import org.tweetyproject.arg.delp.syntax.DefeasibleLogicProgram;
import org.tweetyproject.logics.fol.syntax.FolFormula;
import java.io.FileReader;

/** parse a DeLP program, answer the query literals given as arguments (YES / NO / UNDECIDED / UNKNOWN) */
public class DelpRun {
  public static void main(String[] args) throws Exception {
    DelpParser parser = new DelpParser();
    DefeasibleLogicProgram delp = parser.parseBeliefBase(new FileReader(args[0]));
    DelpReasoner reasoner = new DelpReasoner(new GeneralizedSpecificity());
    for (int i = 1; i < args.length; i++) {
      long t0 = System.currentTimeMillis();
      FolFormula f = (FolFormula) parser.parseFormula(args[i]);
      DelpAnswer.Type ans = reasoner.query(delp, f);
      System.out.println(args[i] + " : " + ans + " (" + (System.currentTimeMillis() - t0) + " ms)");
    }
  }
}
