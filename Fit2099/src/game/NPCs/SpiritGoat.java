package game.NPCs;


import edu.monash.fit2099.engine.actors.Actor;
import game.Actions.CureAction;
import game.GroundEntity.Curable;
import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actions.DoNothingAction;
import edu.monash.fit2099.engine.actors.Behaviour;
import edu.monash.fit2099.engine.displays.Display;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Location;
import game.Actions.DecayAction;
import game.Behaviours.Status;
import game.Behaviours.WanderBehaviour;


import java.util.HashMap;
import java.util.Map;

public class SpiritGoat extends NPC implements Curable {
    private int lifespan = 10;

    private Map<Integer, Behaviour> behaviours = new HashMap<>();
    public SpiritGoat() {
        super("Spirit Goat", 'y', 50);
        addCapability(Status.NON_HOSTILE);
        this.behaviours.put(999, new WanderBehaviour());
        this.addCapability(Status.CURABLE);
    }

    @Override
    public Action playTurn(ActionList actions, Action lastAction, GameMap map, Display display) {
        lifespan--;
        if (lifespan == 0) {
            return new DecayAction();
        }
        for (Behaviour behaviour : behaviours.values()) {
            Action action = behaviour.getAction(this, map);
            if(action != null)
                return action;
        }
        return new DoNothingAction();
    }

    public void tick(Location location) {
        lifespan--;
        if (lifespan == 0) {
            location.map().removeActor(this);
            System.out.println("The SpiritGoat has decayed");
        }
    }
    @Override
    public void cure(Actor user, GameMap map){
        lifespan = 10;
    }
    @Override
    public ActionList allowableActions(Actor otherActor, String direction, GameMap map) {
        ActionList actions = super.allowableActions(otherActor, direction, map);
        // Only allow curing if the other actor has a Talisman (Status.CURE)
        if (otherActor.hasCapability(Status.CURE)) {
            actions.add(new CureAction(this));
        }

        return actions;
    }
}

