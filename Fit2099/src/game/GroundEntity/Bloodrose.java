package game.GroundEntity;

import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.Exit;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Location;
/**
 * Subclass of Crop this represents a BloodRose Ground Object.
 * @author Angus Ashby
 */
public class Bloodrose extends Crop {
    public Bloodrose() {
        super('w');
    }
    /**
     * Provides StaminaCost to plant
     * @return int - StaminaCost
     */
    @Override
    public int getStaminaCost() {
        return 75;
    }
    /**
     * Initial Plant Action on the Map
     * @param location The location the plant is
     * @param map The map the plant is on
     * @param actor the Actor near the plant
     */
    @Override
    public void blooms(Location location, Actor actor, GameMap map) {
        // Sap the farmer’s health by 5 once when planted
        actor.hurt(5);
        if (!actor.isConscious()) {
            actor.unconscious(actor, map);
        }
    }
    /**
     * Perform the Action.
     * @param location The location of the Plant
     */
    @Override
    public void tick(Location location) {
        // Damage nearby actors by 10 each turn
        for (Exit exit : location.getExits()) {
            Actor nearby = exit.getDestination().getActor();
            if (nearby != null) {
                nearby.hurt(10);
                if (!nearby.isConscious()) {
                    GameMap map = exit.getDestination().map();
                    nearby.unconscious(null, map);
                }
            }
        }
    }
}
