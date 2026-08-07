package game.Items;

import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.items.Item;
import edu.monash.fit2099.engine.positions.GameMap;
import game.Actions.CureGroundAction;
import game.Behaviours.Status;
import game.GroundEntity.EntityType;

/**
 * A class representing a Talisman that an actor can pick up and drop
 * @author Adrian Kristanto
 * {@code @edit} Angus Ashby
 */
public class Talisman extends Item {
    public Talisman() {
        super("Talisman", 'o', true);
        this.addCapability(Status.CURE);
    }
    /**
     * List of allowable actions that the item can perform to its owner
     * or to the current map while being carried by an actor
     * Example #1: a healing item can have a special skill that can increase the current actor's hitpoints.
     *
     * @param owner the actor that owns the item
     * @param map the map where the actor is performing the action on
     * @return an unmodifiable list of Actions
     */
    @Override
    public ActionList allowableActions(Actor owner, GameMap map) {
        ActionList actions = new ActionList();
        if (map.locationOf(owner).getGround().hasCapability(EntityType.CURSED)) {
            actions.add(new CureGroundAction());
        }
        return actions;
    }
}





