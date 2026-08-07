package game.Actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.actors.attributes.ActorAttributeOperations;
import edu.monash.fit2099.engine.actors.attributes.BaseActorAttributes;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Location;
import game.GroundEntity.EntityType;
import game.GroundEntity.Soil;

/**
 * Class representing an action to Cure a ground object.
 * Note that the ground must be Cursed and the actor
 * Must have the required Stamina.
 * @author Angus Ashby
 */

public class CureGroundAction extends Action {
    private static final int STAMINA_COST = 50;

    @Override
    public String execute(Actor actor, GameMap map) {
        Location here = map.locationOf(actor);
        if (!here.getGround().hasCapability(EntityType.CURSED)) {
            return "The ground doesn't need curing.";
        }

        int currentStamina = actor.getAttribute(BaseActorAttributes.STAMINA);
        if (currentStamina < STAMINA_COST) {
            return actor + " is too exhausted to use the Talisman.";
        }
        // Reduce stamina
        actor.modifyAttribute(BaseActorAttributes.STAMINA, ActorAttributeOperations.DECREASE, STAMINA_COST);
        // Cure the soil
        here.setGround(new Soil());
        return actor + " cures the blighted soil and loses " + STAMINA_COST + " stamina.";
    }

    @Override
    public String menuDescription(Actor actor) {
        return actor + " uses the Talisman to cure the ground.";
    }
}
