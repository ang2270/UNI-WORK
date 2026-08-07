package game.Actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
/**
 * Class representing an action to remove an Actor
 * From the map.
 * @author Angus Ashby
 */

public class DecayAction extends Action {

    @Override
    public String execute(Actor actor, GameMap map) {
        map.removeActor(actor);
        return actor + " has decayed and withered away.";
    }

    @Override
    public String menuDescription(Actor actor) {
        return actor + " decays.";
    }
}