package game.Items;

import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.items.Item;
import edu.monash.fit2099.engine.positions.Exit;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Location;
import game.Actions.PlantCropAction;
import game.GroundEntity.Crop;
import game.GroundEntity.EntityType;

/**
 * Abstract class representing a generic plantable seed item.
 */
public abstract class SeedItem extends Item {

    private final Crop cropToPlant;
    private final String cropName;

    /**
     * Constructor.
     *
     * @param name the name of the seed item
     * @param displayChar character to represent the seed
     * @param portable whether the item can be picked up
     * @param crop the crop this seed will plant
     * @param cropName the name of the crop (for display)
     */
    public SeedItem(String name, char displayChar, boolean portable, Crop crop, String cropName) {
        super(name, displayChar, portable);
        this.cropToPlant = crop;
        this.cropName = cropName;
    }

    @Override
    public ActionList allowableActions(Actor owner, GameMap map) {
        ActionList actions = new ActionList();
        Location here = map.locationOf(owner);
        if (here.getGround().hasCapability(EntityType.SOIL)) {
            actions.add(new PlantCropAction(newInstanceOfCrop(), cropName, this));
        }

        return actions;
    }

    @Override
    public ActionList allowableActions(Location location) {
        ActionList actions = new ActionList();

        if (location.getGround().hasCapability(EntityType.SOIL)) {
            actions.add(new PlantCropAction(newInstanceOfCrop(), cropName, this));
        }

        return actions;
    }

    /**
     * Return a new instance of the crop to plant. Subclasses should implement this to return the correct type.
     */
    protected abstract Crop newInstanceOfCrop();
}