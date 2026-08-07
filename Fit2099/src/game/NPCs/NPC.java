package game.NPCs;

import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import game.Actions.AttackAction;
import game.Behaviours.Status;


public abstract class NPC extends Actor {

    private final int maxHitPoints;
    private int currentHitPoints;

    public NPC(String name, char displayChar, int maxHitPoints) {
        super(name, displayChar, maxHitPoints);
        this.maxHitPoints = maxHitPoints;
        this.currentHitPoints = maxHitPoints;  // Starts full health
    }

    @Override
    public ActionList allowableActions(Actor otherActor, String direction, GameMap map) {
        ActionList actions = new ActionList();
        // If the attacker has the right status (e.g. Player with HOSTILE_TO_ENEMY)
        if (otherActor.hasCapability(Status.HOSTILE_TO_ENEMY)) {
            actions.add(new AttackAction(this, direction));
        }
        return actions;
    }
}

