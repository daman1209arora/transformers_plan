

(define (problem BW-rand-8)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 )
(:init
(arm-empty)
(on b1 b2)
(on b2 b3)
(on b3 b4)
(on b4 b8)
(on b5 b7)
(on-table b6)
(on b7 b6)
(on b8 b5)
(clear b1)
)
(:goal
(and
(on b1 b3)
(on b2 b4)
(on b3 b7)
(on b4 b6)
(on b5 b8)
(on b6 b1))
)
)


