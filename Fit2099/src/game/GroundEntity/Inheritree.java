package game.GroundEntity;

import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.actors.attributes.ActorAttributeOperations;
import edu.monash.fit2099.engine.actors.attributes.BaseActorAttributes;
import edu.monash.fit2099.engine.positions.Exit;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Location;
/**
 * Subclass of Crop to represent the Inheritree object.
 * @author Angus Ashby
 */
public class Inheritree extends Crop {
    public Inheritree() {
        super('t');
    }
    /**
     * Provides StaminaCost to plant
     * @return int - StaminaCost
     */
    @Override
    public int getStaminaCost() {
        return 25;
    }
    /**
     * Initial Plant Action on the Map
     * @param location The location the plant is
     * @param map The map the plant is on
     * @param actor the Actor near the plant
     */
    @Override
    public void blooms(Location location, Actor actor, GameMap map) {
        for (Exit exit : location.getExits()) {
            Location adjacent = exit.getDestination();
            if (adjacent.getGround().hasCapability(EntityType.CURSED)) {
                adjacent.setGround(new Soil());
            }
        }
    }
    /**
     * Perform the Action.
     * @param location The location of the Plant
     */
    @Override
    public void tick(Location location) {
        for (Exit exit : location.getExits()) {
            Actor nearby = exit.getDestination().getActor();
            if (nearby != null) {
                nearby.heal(5);
                if (nearby.hasAttribute(BaseActorAttributes.STAMINA)){
                    nearby.modifyAttribute(BaseActorAttributes.STAMINA, ActorAttributeOperations.INCREASE, 5);
                }
            }
        }
    }
}

