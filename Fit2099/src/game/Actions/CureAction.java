package game.Actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import game.GroundEntity.Curable;

/**
 * Class representing an action to Cure something.
 * Note that the curable object must be Curable
 * @author Angus Ashby
 */

public class CureAction extends Action {
    private final Curable target;
    /**
     * Constructor.
     *
     * @param target the object to be cured
     */
    public CureAction(Curable target) {
        this.target = target;
    }

    @Override
    public String execute(Actor actor, GameMap map) {
        // Assume target has a cure() method via capability, or it resets countdown, etc.
        if (target != null) {
            target.cure(actor, map);
            return actor + " uses the Talisman to cure " + target + ".";

        }
        return "Nothing happened.";
    }
    @Override
    public String menuDescription(Actor actor) {
        return actor + " uses the Talisman to cure " + target;
    }
}