describe("Shift.isClaimable", function() {
  before(function() {
      window.django_user = new Backbone.Model({id: 1, display_name: "test user"});
  });

  after(function() {
      delete window.django_user;
  });

  it("should not be claimable if locked", function() {
    var shift = new app.Shift({is_locked: true, open_slot_count: 0});
    chai.expect(shift.isClaimable()).to.be.false;
  });

  it("should not be claimable if locked even if has open slots", function() {
    var shift = new app.Shift({is_locked: true, open_slot_count: 1});
    chai.expect(shift.isClaimable()).to.be.false;
  });

  it("should not be claimable if no open slots and not locked", function() {
    var shift = new app.Shift({is_locked: false, open_slot_count: 0});
    chai.expect(shift.isClaimable()).to.be.false;
  });

  it("should be claimable if unlocked and has open slots", function() {
    var shift = new app.Shift({is_locked: false, open_slot_count: 1});
    chai.expect(shift.isClaimable()).to.be.true;
  });
});

