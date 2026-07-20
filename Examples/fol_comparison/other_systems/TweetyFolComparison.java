import java.nio.file.Files;
import java.nio.file.Path;

import org.tweetyproject.logics.commons.syntax.Constant;
import org.tweetyproject.logics.commons.syntax.Functor;
import org.tweetyproject.logics.commons.syntax.Predicate;
import org.tweetyproject.logics.fol.parser.TPTPParser;
import org.tweetyproject.logics.fol.reasoner.SimpleFolReasoner;
import org.tweetyproject.logics.fol.syntax.EqualityPredicate;
import org.tweetyproject.logics.fol.syntax.FolBeliefSet;
import org.tweetyproject.logics.fol.syntax.FolFormula;
import org.tweetyproject.logics.fol.syntax.FolSignature;
import org.tweetyproject.logics.fol.syntax.InequalityPredicate;

public final class TweetyFolComparison {
    private static final class LockedFolSignature extends FolSignature {
        LockedFolSignature() {
            super();
            super.add(new EqualityPredicate());
            super.add(new InequalityPredicate());
        }

        @Override
        public void add(Object symbol) {
            if (symbol instanceof Predicate
                    && containsPredicate(((Predicate) symbol).getName())) {
                return;
            }
            if (symbol instanceof Functor
                    && containsFunctor(((Functor) symbol).getName())) {
                return;
            }
            if (symbol instanceof Constant
                    && containsConstant(((Constant) symbol).get())) {
                return;
            }
            super.add(symbol);
        }
    }

    private static FolSignature readSignature(String filename) throws Exception {
        FolSignature signature = new LockedFolSignature();
        for (String line : Files.readAllLines(Path.of(filename))) {
            if (!line.startsWith("% tweety_signature ")) {
                continue;
            }
            String[] fields = line.split(" ");
            if (fields[2].equals("constant")) {
                signature.add(new Constant(fields[3]));
            } else if (fields[2].equals("functor")) {
                signature.add(new Functor(fields[3], Integer.parseInt(fields[4])));
            } else if (fields[2].equals("predicate")) {
                signature.add(new Predicate(fields[3], Integer.parseInt(fields[4])));
            } else {
                throw new IllegalArgumentException("unknown signature entry: " + line);
            }
        }
        return signature;
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            System.err.println("usage: TweetyFolComparison PROBLEM.p");
            System.exit(2);
        }

        TPTPParser parser = new TPTPParser();
        parser.setSignature(readSignature(args[0]));
        parser.setFormulaRoles(
                "axiom|hypothesis|definition|assumption|lemma|theorem|corollary");
        FolBeliefSet axioms = parser.parseBeliefBaseFromFile(args[0]);
        parser.setFormulaRoles("conjecture");
        FolBeliefSet conjectures = parser.parseBeliefBaseFromFile(args[0]);
        if (conjectures.size() != 1) {
            throw new IllegalArgumentException("expected one conjecture");
        }
        FolFormula conjecture = conjectures.iterator().next();
        System.out.printf("axioms=%d query=%s%n", axioms.size(), conjecture);
        System.out.println("entailed=" + new SimpleFolReasoner().query(axioms, conjecture));
    }
}
