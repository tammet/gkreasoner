import org.tweetyproject.arg.delp.parser.DelpParser;
import org.tweetyproject.arg.delp.reasoner.DelpReasoner;
import org.tweetyproject.arg.delp.semantics.GeneralizedSpecificity;
import org.tweetyproject.arg.delp.syntax.DefeasibleLogicProgram;
import org.tweetyproject.commons.InferenceMode;
import org.tweetyproject.logics.fol.reasoner.FolReasoner;
import org.tweetyproject.logics.fol.reasoner.SimpleFolReasoner;
import org.tweetyproject.logics.fol.syntax.FolFormula;
import org.tweetyproject.logics.rdl.parser.RdlParser;
import org.tweetyproject.logics.rdl.reasoner.SimpleDefaultReasoner;
import org.tweetyproject.logics.rdl.syntax.DefaultTheory;

public final class TweetyComparison {
    private static void queryRdl(
            SimpleDefaultReasoner reasoner,
            RdlParser parser,
            DefaultTheory theory,
            String text) throws Exception {
        FolFormula formula = (FolFormula) parser.parseFormula(text);
        System.out.printf(
                "RDL %-15s skeptical=%-5s credulous=%-5s%n",
                text,
                reasoner.query(theory, formula, InferenceMode.SKEPTICAL),
                reasoner.query(theory, formula, InferenceMode.CREDULOUS));
    }

    private static void queryDelp(
            DelpReasoner reasoner,
            DelpParser parser,
            DefeasibleLogicProgram program,
            String text) throws Exception {
        FolFormula formula = (FolFormula) parser.parseFormula(text);
        System.out.printf(
                "DeLP %-23s answer=%s%n",
                text,
                reasoner.query(program, formula));
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 3) {
            System.err.println(
                    "usage: TweetyComparison BIRDS.rdl BIRDS.delp NIXON.delp");
            System.exit(2);
        }

        FolReasoner.setDefaultReasoner(new SimpleFolReasoner());

        RdlParser rdlParser = new RdlParser();
        DefaultTheory rdlTheory = rdlParser.parseBeliefBaseFromFile(args[0]);
        SimpleDefaultReasoner rdlReasoner = new SimpleDefaultReasoner();
        System.out.println("RDL extensions=" + rdlReasoner.getModels(rdlTheory).size());
        queryRdl(rdlReasoner, rdlParser, rdlTheory, "Flies(tweety)");
        queryRdl(rdlReasoner, rdlParser, rdlTheory, "Flies(opus)");
        queryRdl(rdlReasoner, rdlParser, rdlTheory, "!Flies(opus)");

        DelpParser delpParser = new DelpParser();
        DelpReasoner delpReasoner =
                new DelpReasoner(new GeneralizedSpecificity());
        DefeasibleLogicProgram birds =
                delpParser.parseBeliefBaseFromFile(args[1]);
        queryDelp(delpReasoner, delpParser, birds, "Flies(tweety)");
        queryDelp(delpReasoner, delpParser, birds, "~Flies(tweety)");
        queryDelp(delpReasoner, delpParser, birds, "Flies(opus)");
        queryDelp(delpReasoner, delpParser, birds, "~Flies(opus)");

        DefeasibleLogicProgram nixon =
                delpParser.parseBeliefBaseFromFile(args[2]);
        queryDelp(delpReasoner, delpParser, nixon, "pacifist(nixon)");
        queryDelp(delpReasoner, delpParser, nixon, "~pacifist(nixon)");
    }
}
