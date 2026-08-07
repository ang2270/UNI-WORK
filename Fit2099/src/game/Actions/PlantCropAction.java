package game.Actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.actors.attributes.ActorAttributeOperations;
import edu.monash.fit2099.engine.actors.attributes.BaseActorAttributes;
import edu.monash.fit2099.engine.items.Item;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Location;
import game.GroundEntity.Crop;
import game.GroundEntity.EntityType;

/**
 * Class representing an action to Plant a Crop
 * Note that the object must be of Type Crop and
 * the Actor must have enough Stamina.
 * @author Angus Ashby
 */

public class PlantCropAction extends Action {
    private final Crop crop;
    private final String cropName;
    private final Item seedItem;

    /**
     * Constructor
     *
     * @param crop the crop to to be planted
     * @param cropName the name of the Crop being planted (only used for display purposes)
     * @param seedItem The seedItem the crop is coming from
     */

    public PlantCropAction(Crop crop, String cropName, Item seedItem) {
        this.crop = crop;
        this.cropName = cropName;
        this.seedItem = seedItem;
    }

    @Override
    public String execute(Actor actor, GameMap map) {
        Location location = map.locationOf(actor);
        if (!(location.getGround().hasCapability(EntityType.SOIL))) {
            return "You can't plant seeds here.";
        }
        int currentStamina = actor.getAttribute(BaseActorAttributes.STAMINA);
        int requiredStamina = crop.getStaminaCost();

        if (currentStamina < requiredStamina) {
            return "You do not have enough stamina to plant " + crop.getClass().getSimpleName() + ".";
        }

        actor.modifyAttribute(BaseActorAttributes.STAMINA, ActorAttributeOperations.DECREASE, requiredStamina);

        location.setGround(crop);
        actor.removeItemFromInventory(seedItem);
        crop.blooms(location, actor, map);
        return "You planted a " + cropName + "!";
    }

    @Override
    public String menuDescription(Actor actor) {
        return actor + " plants a " + cropName;
    }
}
