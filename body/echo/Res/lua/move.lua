local Move = 
{
	posX = 10,
	step = 0.2,
}

-- start
function Move:start()
	--Log:error(type(Log))
	--Log:error(type(Log.error))

	--for k,v in pairs(getmetatable(Log)) do
		--Log:error( k .. "->" .. type(v))
	--end
end

-- update
function Move:update()
	if self.posX > 250 then
		self.posX = 10
	end

	if Input:isMouseButtonDown(0) then
		self.step = -self.step
	end

	self.posX = self.posX + self.step
	--self:setWorldPositionX(self.posX)
end

return Move